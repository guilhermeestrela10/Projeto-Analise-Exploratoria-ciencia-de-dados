"""Atributos interpretáveis e transformações demonstrativas separadas."""
# [IA] registro 1
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def engineer(d):
    d = d.copy()
    seconds = 86400
    approved = d.order_approved_at
    carrier = d.order_delivered_carrier_date
    customer = d.order_delivered_customer_date
    purchase = d.order_purchase_timestamp
    limit = d.shipping_limit_date
    chronology = purchase.notna() & approved.ge(purchase) & carrier.ge(approved)
    d['invalid_chronology'] = ((approved < purchase) | (carrier < approved) |
        (customer < carrier) | (limit < approved)).fillna(False)
    dispatch_valid = chronology & limit.ge(approved) & d.deadlines_complete
    dispatch_valid &= d.order_status.isin(['delivered', 'shipped'])
    d['approval_to_carrier_days'] = ((carrier - approved).dt.total_seconds() / seconds).where(chronology)
    d['dispatch_delay_days'] = ((carrier - limit).dt.total_seconds() / seconds).where(dispatch_valid)
    d['dispatch_late'] = (d.dispatch_delay_days > 0).astype('Int64').where(d.dispatch_delay_days.notna())
    d['eligible_dispatch'] = dispatch_valid & d.seller_count.eq(1) & d.seller_id.notna()
    transport_valid = carrier.notna() & customer.ge(carrier)
    d['transport_days'] = ((customer - carrier).dt.total_seconds() / seconds).where(transport_valid)
    d['delivery_days'] = ((customer - purchase).dt.total_seconds() / seconds).where(customer.ge(purchase))
    # O prazo estimado é uma data; entregar no mesmo dia não conta como atraso.
    delivery_valid = customer.notna() & d.order_estimated_delivery_date.notna() & customer.ge(purchase)
    d['delivery_late'] = (customer.dt.normalize() > d.order_estimated_delivery_date.dt.normalize()).astype('Int64').where(delivery_valid)
    d['negative_review'] = d.review_score.le(2).astype('Int64').where(d.review_score.notna())
    d['eligible_review'] = d.eligible_dispatch & d.review_score.notna()
    d['purchase_month'] = purchase.dt.strftime('%Y-%m').astype('string')
    d['purchase_weekday'] = purchase.dt.dayofweek.astype('Int64')
    d['freight_share'] = d.freight_value.div(d.sales_value + d.freight_value).where((d.sales_value + d.freight_value) > 0)
    valid = d.loc[d.eligible_dispatch, 'approval_to_carrier_days'].dropna()
    q1, q3 = valid.quantile(.25), valid.quantile(.75)
    lower, upper = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    d['dispatch_time_outlier'] = ((d.approval_to_carrier_days < lower) | (d.approval_to_carrier_days > upper)).where(d.eligible_dispatch, False)
    d['demo_dispatch_clipped'] = d.approval_to_carrier_days.clip(lower=lower, upper=upper)
    for name, scaler in [('minmax', MinMaxScaler()), ('zscore', StandardScaler())]:
        d[f'demo_sales_{name}'] = np.nan
        mask = d.sales_value.notna()
        if mask.any():
            d.loc[mask, f'demo_sales_{name}'] = scaler.fit_transform(d.loc[mask, ['sales_value']]).ravel()
    status = d.order_status.where(d.order_status.isin(['delivered', 'shipped']), 'other')
    encoded = pd.get_dummies(pd.Categorical(status, categories=['delivered', 'shipped', 'other']), prefix='demo_status', dtype=int)
    for col in encoded:
        d[col] = encoded[col].to_numpy()
    d.attrs['outlier_bounds'] = {'lower': lower, 'upper': upper, 'reference_n': len(valid)}
    return d
