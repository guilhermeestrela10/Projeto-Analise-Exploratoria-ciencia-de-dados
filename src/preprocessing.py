"""Pipeline único: brutos -> uma linha por pedido e vendedor observado."""
# [IA] registro 1
import numpy as np
import pandas as pd
from .feature_engineering import engineer

ORDER_DATES = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
               'order_delivered_customer_date', 'order_estimated_delivery_date']
REQUIRED = {
    'orders': ['order_id', 'order_status', *ORDER_DATES],
    'items': ['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value'],
    'products': ['product_id', 'product_category_name'],
    'sellers': ['seller_id', 'seller_state'],
    'reviews': ['order_id', 'review_id', 'review_score', 'review_answer_timestamp', 'review_comment_message']}
KEYS = {'orders': ['order_id'], 'items': ['order_id', 'order_item_id'],
        'products': ['product_id'], 'sellers': ['seller_id']}


def profile(df):
    return {'rows': len(df), 'columns': len(df.columns), 'duplicates': int(df.duplicated().sum()),
            'nulls': {c: int(v) for c, v in df.isna().sum().items()},
            'types': {c: str(v) for c, v in df.dtypes.items()}}


def preprocessar(orders, items, products, sellers, reviews):
    """Recebe DataFrames originais; não altera os argumentos. Evidências em attrs['audit']."""
    raw = dict(zip(REQUIRED, [orders, items, products, sellers, reviews]))
    audit = {'before': {k: profile(v) for k, v in raw.items()}, 'invalid_dates': {}, 'null_keys_removed': {}}
    cleaned = {}
    for name, frame in raw.items():
        missing = set(REQUIRED[name]) - set(frame.columns)
        if missing:
            raise ValueError(f'{name}: colunas obrigatórias ausentes: {", ".join(sorted(missing))}')
        # Limitar colunas também evita propagar identificadores pessoais e textos livres.
        df = frame.drop_duplicates().loc[:, REQUIRED[name]].copy()
        for c in [c for c in df if c.endswith('_id')]:
            df[c] = df[c].astype('string').str.strip().replace('', pd.NA)
        key = KEYS.get(name, ['order_id', 'review_id'])
        audit['null_keys_removed'][name] = int(df[key].isna().any(axis=1).sum())
        df = df.dropna(subset=key).drop_duplicates()
        if name in KEYS and df.duplicated(key).any():
            raise ValueError(f'{name}: chave conflitante {key}; resolver na origem, sem escolher uma linha arbitrariamente.')
        dates = [c for c in df if c in ORDER_DATES or c in ['shipping_limit_date', 'review_answer_timestamp']]
        for c in dates:
            parsed = pd.to_datetime(df[c], errors='coerce', format='mixed')
            audit['invalid_dates'][f'{name}.{c}'] = int((df[c].notna() & parsed.isna()).sum())
            df[c] = parsed
        cleaned[name] = df
    o, i, p, s, r = (cleaned[k] for k in REQUIRED)
    o['order_status'] = o.order_status.astype('string').str.strip().str.lower().fillna('unknown')
    p['product_category_name'] = p.product_category_name.astype('string').str.strip().str.lower().replace('', pd.NA).fillna('sem_categoria')
    s['seller_state'] = s.seller_state.astype('string').str.strip().str.upper()
    states = 'AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO'.split()
    s['seller_state'] = s.seller_state.where(s.seller_state.isin(states), 'SEM_INFORMACAO')
    for c in ['price', 'freight_value']:
        values = pd.to_numeric(i[c], errors='coerce').astype(float)
        valid = np.isfinite(values) & values.ge(0)
        audit[f'invalid_{c}'] = int((i[c].notna() & ~valid).sum())
        i[c] = values.where(valid)
    scores = pd.to_numeric(r.review_score, errors='coerce').astype(float)
    r['review_score'] = scores.where(scores.isin([1, 2, 3, 4, 5]))
    audit['invalid_review_scores'] = int((scores.notna() & r.review_score.isna()).sum())
    text = r.review_comment_message.astype('string').str.normalize('NFKC').str.replace(r'\s+', ' ', regex=True).str.strip().str.lower()
    r['review_text_length'] = text.str.len().fillna(0).astype(int)
    audit['reviews_reduced'] = int(r.duplicated('order_id').sum())
    # Última resposta conhecida; empates por ID, nota e tamanho. NaT não vence uma data válida.
    r = r.sort_values(['order_id', 'review_answer_timestamp', 'review_id', 'review_score', 'review_text_length'], na_position='first').drop_duplicates('order_id', keep='last')
    r = r[['order_id', 'review_score', 'review_text_length']]
    audit['orphan_items'] = int((~i.order_id.isin(o.order_id)).sum())
    audit['missing_products'] = int((~i.product_id.isin(p.product_id)).sum())
    audit['missing_sellers'] = int((~i.seller_id.isin(s.seller_id)).sum())
    audit['items_unknown_seller'] = int(i.seller_id.isna().sum())
    audit['orders_without_items'] = int((~o.order_id.isin(i.order_id)).sum())
    audit['reviews_without_orders'] = int((~r.order_id.isin(o.order_id)).sum())
    i = i[i.order_id.isin(o.order_id)].merge(p, on='product_id', how='left', validate='many_to_one')
    i['product_category_name'] = i.product_category_name.fillna('sem_categoria')
    # Soma só é publicada se todos os itens do grupo possuírem valor válido.
    def complete_sum(values):
        return values.sum() if values.notna().all() else float('nan')
    pairs = i.groupby(['order_id', 'seller_id'], sort=True, dropna=False).agg(
        item_count=('order_item_id', 'size'), sales_value=('price', complete_sum),
        freight_value=('freight_value', complete_sum), shipping_limit_date=('shipping_limit_date', 'min'),
        shipping_limit_max=('shipping_limit_date', 'max'),
        deadlines_complete=('shipping_limit_date', lambda x: x.notna().all()),
        category_count=('product_category_name', 'nunique'),
        category_main=('product_category_name', lambda x: x.mode().sort_values().iloc[0])).reset_index()
    # Agregações vazias podem herdar datetime da coluna de origem.
    pairs['deadlines_complete'] = pairs.deadlines_complete.astype(bool)
    for c in ['item_count', 'sales_value', 'freight_value', 'category_count']:
        pairs[c] = pd.to_numeric(pairs[c], errors='coerce')
    counts = i.groupby('order_id').agg(seller_count=('seller_id', lambda x: x.nunique(dropna=False)), order_item_count=('order_item_id', 'size')).reset_index()
    d = pairs.merge(counts, on='order_id', validate='many_to_one').merge(o, on='order_id', validate='many_to_one')
    d = d.merge(s, on='seller_id', how='left', validate='many_to_one').merge(r, on='order_id', how='left', validate='many_to_one')
    d['seller_state'] = d.seller_state.fillna('SEM_INFORMACAO')
    if d.duplicated(['order_id', 'seller_id']).any():
        raise ValueError('Granularidade inválida após os merges.')
    d = engineer(d)
    bounds = d.attrs.get('outlier_bounds', {})
    d = d.sort_values(['order_id', 'seller_id']).reset_index(drop=True)
    audit['after'] = {k: profile(v) for k, v in cleaned.items()}
    audit['final'] = profile(d)
    audit['outlier_bounds'] = bounds
    audit['eligible_dispatch'] = int(d.eligible_dispatch.sum())
    audit['eligible_review'] = int(d.eligible_review.sum())
    audit['multi_seller_orders'] = int(d.loc[d.seller_count.gt(1), 'order_id'].nunique())
    audit['invalid_chronology_pairs'] = int(d.invalid_chronology.sum())
    d.attrs['audit'] = audit
    return d
