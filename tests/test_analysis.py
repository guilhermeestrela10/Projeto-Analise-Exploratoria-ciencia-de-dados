# [IA] registro 2
import pandas as pd
import pytest
from src.analysis import seller_metrics, review_comparison, filter_data
from src.preprocessing import preprocessar
from test_preprocessing import raw


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
