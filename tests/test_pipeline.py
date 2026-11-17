# [IA] registro 3
from pathlib import Path
import pandas as pd
from src.load_data import load_data, ROOT
from src.preprocessing import preprocessar
from src.reporting import FIELD_INFO, write_outputs
from test_preprocessing import raw


def test_real_small_sample_and_output(tmp_path):
    orders, items, products, sellers, reviews = load_data()
    orders = orders.sample(50, random_state=4)
    items = items[items.order_id.isin(orders.order_id)]
    products = products[products.product_id.isin(items.product_id)]
    sellers = sellers[sellers.seller_id.isin(items.seller_id)]
    reviews = reviews[reviews.order_id.isin(orders.order_id)]
    d = preprocessar(orders, items, products, sellers, reviews)
    assert len(d) == items[['order_id', 'seller_id']].drop_duplicates().shape[0]
    assert d.order_id.isin(orders.order_id).all()
    assert d.loc[d.eligible_dispatch, 'dispatch_late'].isin([0, 1]).all()
    assert set(d.columns) == set(FIELD_INFO)
    write_outputs(d, (orders, items, products, sellers, reviews), tmp_path, charts=False)
    restored = pd.read_csv(tmp_path / 'data/processed/tabela_analitica.csv')
    assert len(restored) == len(d)
    assert (tmp_path / 'reports/dicionario_de_dados.md').is_file()
    # Recorte independente simula dimensões sem correspondência, preservando o esquema.
    partial = preprocessar(orders.iloc[:2], items.iloc[:1], products.iloc[:0], sellers.iloc[:0], reviews.iloc[:0])
    assert len(partial) <= 1


def test_single_real_order_and_no_common_orders():
    orders, items, products, sellers, reviews = load_data()
    first = items.iloc[:1]
    o = orders[orders.order_id.isin(first.order_id)]
    d = preprocessar(o, first, products, sellers, reviews)
    assert len(d) == 1
    assert d.demo_sales_minmax.eq(0).all()
    assert d.demo_sales_zscore.eq(0).all()
    empty = preprocessar(orders[~orders.order_id.isin(first.order_id)].iloc[:1], first, products, sellers, reviews)
    assert empty.empty


def test_deadline_sensitivity_is_measured(raw, tmp_path):
    raw[1].loc[1, 'shipping_limit_date'] = '2018-01-07'
    d = preprocessar(*raw)
    write_outputs(d, raw, tmp_path, charts=False)
    comparison = pd.read_csv(tmp_path / 'reports/comparacao_prazos.csv').set_index('referencia')
    assert comparison.loc['menor_prazo', 'atrasos'] == 1
    assert comparison.loc['maior_prazo', 'atrasos'] == 0
    assert comparison.loc['menor_prazo', 'pedidos_elegiveis'] == 2
