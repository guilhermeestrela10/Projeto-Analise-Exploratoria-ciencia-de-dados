# [IA] registro 2
import pandas as pd
import pytest
from src.analysis import seller_metrics, review_comparison, filter_data
from src.preprocessing import preprocessar
from test_preprocessing import raw


# [IA] registro 5
def test_monitoring_uses_thirty_day_window_and_business_days(raw):
    from src.analysis import monitoring_metrics
    raw[0].loc[0, 'order_purchase_timestamp'] = '2018-01-05'
    raw[0].loc[0, 'order_approved_at'] = '2018-01-05'
    raw[0].loc[0, 'order_delivered_carrier_date'] = '2018-01-08'
    raw[1].loc[raw[1].order_id.eq('a'), 'shipping_limit_date'] = '2018-01-06'
    d = preprocessar(*raw)
    result, start, end = monitoring_metrics(d)
    s = result.set_index('seller_id').loc['s']
    assert s['mean_business_days'] == 1
    assert s['late_rate'] == 1
    assert s['mean_score'] == 2
    assert s['above_tad_limit']
    assert s['below_score_floor']
    assert (end - start).days == 29


def test_monitoring_excludes_orders_outside_window_and_handles_empty(raw):
    from src.analysis import monitoring_metrics
    d = preprocessar(*raw)
    d.loc[d.order_id.eq('a'), 'order_purchase_timestamp'] = pd.Timestamp('2017-01-01')
    result, _, _ = monitoring_metrics(d)
    assert set(result.seller_id) == {'t'}
    result, start, end = monitoring_metrics(d.iloc[:0])
    assert result.empty
    assert start is None and end is None


def test_rates_use_only_eligible_orders(raw):
    d = preprocessar(*raw)
    m = seller_metrics(d).set_index('seller_id')
    assert m.loc['s', 'eligible_orders'] == 1
    assert m.loc['s', 'late_rate'] == 1
    assert m.loc['s', 'negative_rate'] == 1
    c = review_comparison(d).set_index('dispatch_late')
    assert c.loc[1, 'review_count'] == 1
    assert c.loc[0, 'mean_score'] == 5


def test_filters_recompute_metrics(raw):
    d = preprocessar(*raw)
    filtered = filter_data(d, ['PI'], [], None, None)
    assert len(filtered) == 1
    assert seller_metrics(filtered).eligible_orders.sum() == 1
    assert filter_data(d, ['XX'], [], None, None).empty


def test_no_eligible_sample_does_not_divide_by_zero(raw):
    raw[0]['order_delivered_carrier_date'] = None
    d = preprocessar(*raw)
    assert seller_metrics(d).late_rate.isna().all()
    assert review_comparison(d).empty
