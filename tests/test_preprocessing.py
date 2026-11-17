# [IA] registro 1
import numpy as np
import pandas as pd
import pytest

from src.preprocessing import preprocessar


@pytest.fixture
def raw():
    # Dados artificiais exclusivos dos testes; nunca usados nos resultados.
    orders = pd.DataFrame({
        'order_id': ['a', 'b'], 'order_status': ['delivered', 'delivered'],
        'order_purchase_timestamp': ['2018-01-01', '2018-01-02'],
        'order_approved_at': ['2018-01-01', '2018-01-02'],
        'order_delivered_carrier_date': ['2018-01-05', '2018-01-03'],
        'order_delivered_customer_date': ['2018-01-10', '2018-01-08'],
        'order_estimated_delivery_date': ['2018-01-09', '2018-01-10']})
    items = pd.DataFrame({'order_id': ['a', 'a', 'b'], 'order_item_id': [1, 2, 1],
        'product_id': ['p', 'p', 'p'], 'seller_id': ['s', 's', 't'],
        'shipping_limit_date': ['2018-01-04'] * 3, 'price': [10., 20., 30.], 'freight_value': [2.] * 3})
    products = pd.DataFrame({'product_id': ['p'], 'product_category_name': [' CASA ']})
    sellers = pd.DataFrame({'seller_id': ['s', 't'], 'seller_state': [' pi ', 'SP']})
    reviews = pd.DataFrame({'order_id': ['a', 'a', 'b'], 'review_id': ['r1', 'r2', 'r3'],
        'review_score': [1, 2, 5], 'review_answer_timestamp': ['2018-01-11', '2018-01-12', '2018-01-10'],
        'review_comment_message': ['  Muito   RUIM ', None, 'Bom']})
    return [orders, items, products, sellers, reviews]


def test_granularity_and_denominator(raw):
    out = preprocessar(*raw)
    assert len(out) == 2
    a = out.set_index('order_id').loc['a']
    assert a['item_count'] == 2
    assert a['sales_value'] == 30
    assert a['review_score'] == 2
    assert a['dispatch_late'] == 1
    assert a['dispatch_delay_days'] == 1
    assert a['seller_state'] == 'PI'
    assert not out.duplicated(['order_id', 'seller_id']).any()
    assert raw[3].iloc[0]['seller_state'] == ' pi '


def test_multiple_sellers_not_individually_eligible(raw):
    raw[1].loc[1, 'seller_id'] = 't'
    out = preprocessar(*raw)
    a = out[out.order_id == 'a']
    assert len(a) == 2
    assert a.seller_count.eq(2).all()
    assert not a.eligible_dispatch.any()
    assert not a.eligible_review.any()


def test_missing_or_invalid_dispatch_is_unknown(raw):
    raw[0].loc[0, 'order_delivered_carrier_date'] = 'inválida'
    out = preprocessar(*raw).set_index('order_id')
    assert pd.isna(out.loc['a', 'dispatch_late'])
    assert not out.loc['a', 'eligible_dispatch']


def test_constant_and_empty_samples(raw):
    one = preprocessar(raw[0].iloc[:1], raw[1].iloc[:1], *raw[2:])
    assert one['demo_sales_minmax'].eq(0).all()
    assert one['demo_sales_zscore'].eq(0).all()
    empty = preprocessar(*[df.iloc[:0] for df in raw])
    assert empty.empty
    assert set(empty.columns) == set(preprocessar(*raw).columns)


def test_conflicting_dimension_key_rejected(raw):
    raw[2] = pd.concat([raw[2], pd.DataFrame({'product_id': ['p'], 'product_category_name': ['outra']})])
    with pytest.raises(ValueError, match='chave'):
        preprocessar(*raw)


def test_exact_duplicates_do_not_change_results(raw):
    baseline = preprocessar(*raw)
    duplicate = [pd.concat([df, df.iloc[:1]], ignore_index=True) for df in raw]
    pd.testing.assert_frame_equal(baseline, preprocessar(*duplicate))


def test_required_columns(raw):
    raw[1] = raw[1].drop(columns='shipping_limit_date')
    with pytest.raises(ValueError, match='shipping_limit_date'):
        preprocessar(*raw)


def test_negative_chronology_excluded(raw):
    raw[0].loc[0, 'order_delivered_carrier_date'] = '2017-12-01'
    out = preprocessar(*raw).set_index('order_id')
    assert not out.loc['a', 'eligible_dispatch']
    assert pd.isna(out.loc['a', 'dispatch_late'])


def test_orphan_items_and_empty_dimensions(raw):
    raw[1].loc[0, 'order_id'] = 'missing'
    out = preprocessar(raw[0], raw[1], raw[2].iloc[:0], raw[3].iloc[:0], raw[4].iloc[:0])
    assert len(out) == 2
    assert out.review_score.isna().all()
    assert out.seller_state.eq('SEM_INFORMACAO').all()
    assert out.attrs['audit']['orphan_items'] == 1


def test_partial_missing_deadline_not_hidden_by_min(raw):
    raw[1].loc[0, 'shipping_limit_date'] = None
    out = preprocessar(*raw).set_index('order_id')
    assert not out.loc['a', 'eligible_dispatch']


def test_invalid_review_and_money_remain_unknown(raw):
    raw[4].loc[2, 'review_score'] = 9
    raw[1].loc[2, 'price'] = -30
    out = preprocessar(*raw).set_index('order_id')
    assert pd.isna(out.loc['b', 'review_score'])
    assert pd.isna(out.loc['b', 'sales_value'])


def test_infinite_money_becomes_unknown(raw):
    raw[1].loc[0, 'price'] = np.inf
    out = preprocessar(*raw).set_index('order_id')
    assert pd.isna(out.loc['a', 'sales_value'])
    assert out.attrs['audit']['invalid_price'] == 1


def test_unknown_seller_not_dropped_or_assumed_single(raw):
    raw[1].loc[1, 'seller_id'] = None
    out = preprocessar(*raw)
    a = out[out.order_id.eq('a')]
    assert len(a) == 2
    assert a.sales_value.sum() == 30
    assert a.seller_count.eq(2).all()
    assert not a.eligible_dispatch.any()
    raw[1] = raw[1].iloc[[1]]
    unknown = preprocessar(*raw)
    assert len(unknown) == 1
    assert not unknown.eligible_dispatch.any()
