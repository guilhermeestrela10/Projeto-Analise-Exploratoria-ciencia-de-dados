# [IA] registro 2
from pathlib import Path
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('page', ['app.py', 'pages/1_Atrasos_no_Despacho.py',
    'pages/2_Atrasos_e_Avaliacoes.py', 'pages/3_Criterios_para_Vendedores.py'])
def test_pages_and_state_filter(page):
    at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=40).run()
    if page != 'app.py':
        at.switch_page(page).run()
    assert not at.exception
    assert at.metric
    at.multiselect[0].set_value(['PI']).run()
    assert not at.exception
    d = pd.read_csv(ROOT / 'data/processed/tabela_analitica.csv')
    assert int(at.metric[0].value.replace('.', '').replace(',', '')) == d.loc[d.seller_state.eq('PI'), 'order_id'].nunique()
    at.multiselect[1].set_value(['vendedor_inexistente']).run()
    assert not at.exception
    assert at.info


def test_period_filter_and_incomplete_date_range():
    at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=40).run()
    d = pd.read_csv(ROOT / 'data/processed/tabela_analitica.csv', parse_dates=['order_purchase_timestamp'])
    day = d.order_purchase_timestamp.min().date()
    at.date_input[0].set_value((day,)).run()
    assert not at.exception
    assert at.info
    at.date_input[0].set_value((day, day)).run()
    assert not at.exception
    assert int(at.metric[0].value.replace('.', '').replace(',', '')) == d.loc[d.order_purchase_timestamp.dt.date.eq(day), 'order_id'].nunique()
