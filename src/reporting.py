"""Evidências técnicas e documentação reproduzível; não escreve conclusões autorais."""
# [IA] registro 3
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from .analysis import seller_metrics, review_comparison, selection_report
from .preprocessing import REQUIRED
from .visualizations import save_charts

# descrição, origem e tratamento aplicado (Anexo C)
FIELD_INFO = {
 'order_id': ('Identificador do pedido; parte da chave final.', 'orders.order_id / items.order_id', 'Texto sem espaços; chave validada.'),
 'seller_id': ('Identificador do vendedor observado; parte da chave final; pode ser desconhecido.', 'items.seller_id', 'Texto sem espaços; ausências preservadas em grupo próprio e excluídas da comparação individual.'),
 'item_count': ('Quantidade de itens do vendedor neste pedido.', 'items.order_item_id', 'Contagem após remoção de duplicatas exatas.'),
 'sales_value': ('Valor dos itens deste vendedor no pedido, em BRL; não é receita líquida.', 'items.price', 'Soma completa; grupo com valor inválido fica ausente.'),
 'freight_value': ('Frete dos itens deste vendedor no pedido, em BRL.', 'items.freight_value', 'Soma completa; negativos e inválidos viram ausência.'),
 'shipping_limit_date': ('Menor prazo de despacho dos itens deste vendedor.', 'items.shipping_limit_date', 'Conversão segura e mínimo por pedido-vendedor.'),
 'shipping_limit_max': ('Maior prazo de despacho dos itens deste vendedor.', 'items.shipping_limit_date', 'Conversão segura e máximo por pedido-vendedor.'),
 'deadlines_complete': ('Todos os itens do grupo possuem prazo válido.', 'items.shipping_limit_date', 'Indicador booleano; requisito de elegibilidade.'),
 'category_count': ('Número de categorias observadas no grupo.', 'products.product_category_name', 'Contagem distinta, incluindo sem_categoria.'),
 'category_main': ('Categoria mais frequente no grupo; não representa todos os itens.', 'items.product_id / products.product_category_name', 'Texto minúsculo; ausências sem_categoria; empate alfabético.'),
 'seller_count': ('Número de vendedores distintos observados no pedido, incluindo grupo desconhecido.', 'items.seller_id', 'Contagem inclui ausência para impedir falsa identificação de vendedor único; depende da cobertura da amostra.'),
 'order_item_count': ('Quantidade total de itens observados no pedido.', 'items.order_item_id', 'Contagem por pedido; repetida em cada vendedor, não somar entre vendedores.'),
 'order_status': ('Situação do pedido.', 'orders.order_status', 'Minúsculo, espaços externos removidos, ausência unknown.'),
 'order_purchase_timestamp': ('Data e hora da compra; filtro temporal.', 'orders.order_purchase_timestamp', 'to_datetime errors=coerce; sem imputação.'),
 'order_approved_at': ('Data e hora da aprovação.', 'orders.order_approved_at', 'Conversão segura; sem imputação.'),
 'order_delivered_carrier_date': ('Data de entrega à transportadora do pedido, sem detalhe por vendedor.', 'orders.order_delivered_carrier_date', 'Conversão segura; aproximação do despacho individual.'),
 'order_delivered_customer_date': ('Data de entrega ao cliente.', 'orders.order_delivered_customer_date', 'Conversão segura; sem imputação.'),
 'order_estimated_delivery_date': ('Dia previsto para entrega ao cliente.', 'orders.order_estimated_delivery_date', 'Conversão segura; comparação por dia civil.'),
 'seller_state': ('UF do vendedor.', 'sellers.seller_state', 'Maiúsculas; UF inválida ou dimensão ausente SEM_INFORMACAO.'),
 'review_score': ('Nota inteira de 1 a 5, única por pedido; repetida em pedidos multivendedor.', 'reviews.review_score / review_answer_timestamp / review_id', 'Última resposta datada; empates por ID, nota e tamanho; fora de 1..5 ausente.'),
 'review_text_length': ('Comprimento do comentário selecionado após limpeza; sem publicar texto livre.', 'reviews.review_comment_message', 'NFKC, minúsculas, espaços simples; ausência vira comprimento 0; não mede sentimento.'),
 'invalid_chronology': ('Alguma sequência temporal observada é contraditória.', 'Datas de compra, aprovação, despacho, prazo e entrega', 'Sinalizar; cada duração aplica sua própria elegibilidade.'),
 'approval_to_carrier_days': ('Dias corridos entre aprovação e transportadora.', 'order_delivered_carrier_date - order_approved_at', 'Segundos / 86400; exige compra <= aprovação <= despacho.'),
 'dispatch_delay_days': ('Dias corridos de excesso sobre o menor prazo; negativos representam antecedência.', 'order_delivered_carrier_date - shipping_limit_date', 'Exige datas coerentes, prazos completos e status delivered/shipped.'),
 'dispatch_late': ('1 para despacho após o prazo, 0 em prazo, ausente se não mensurável.', 'dispatch_delay_days', 'Comparação estrita > 0; não imputar ausência como zero.'),
 'eligible_dispatch': ('Pedido elegível à comparação individual de despacho.', 'seller_count / datas / deadlines_complete / order_status', 'Um vendedor observado; datas completas e coerentes; delivered ou shipped.'),
 'transport_days': ('Dias entre transportadora e cliente.', 'order_delivered_customer_date - order_delivered_carrier_date', 'Segundos / 86400; somente sequência não negativa.'),
 'delivery_days': ('Dias entre compra e entrega ao cliente.', 'order_delivered_customer_date - order_purchase_timestamp', 'Segundos / 86400; somente sequência não negativa.'),
 'delivery_late': ('1 se entregue depois do dia prometido; ausente se não mensurável.', 'order_delivered_customer_date / order_estimated_delivery_date', 'Datas normalizadas; entrega no mesmo dia não é atraso.'),
 'negative_review': ('1 para nota 1 ou 2; 0 para 3 a 5; ausência preservada.', 'review_score', 'Indicador nullable; não é análise de sentimento.'),
 'eligible_review': ('Elegível para comparar notas e atraso individual de despacho.', 'eligible_dispatch / review_score', 'Despacho elegível e nota válida disponível.'),
 'purchase_month': ('Mês da compra, AAAA-MM.', 'order_purchase_timestamp', 'Extração temporal; sem imputação.'),
 'purchase_weekday': ('Dia da semana da compra: segunda 0, domingo 6.', 'order_purchase_timestamp', 'Extração temporal nullable.'),
 'freight_share': ('Fração do frete no valor de itens mais frete.', 'freight_value / (sales_value + freight_value)', 'Denominador positivo; fração 0..1, não percentual monetário adicional.'),
 'dispatch_time_outlier': ('Tempo de despacho fora das cercas IQR dos pedidos elegíveis do lote.', 'approval_to_carrier_days / eligible_dispatch', 'Q1-1.5 IQR e Q3+1.5 IQR; não exclui linhas.'),
 'demo_dispatch_clipped': ('Tempo de despacho limitado às cercas IQR; somente demonstração.', 'approval_to_carrier_days', 'Clipping; medida original preservada e usada nos indicadores.'),
 'demo_sales_minmax': ('Valor comercializado normalizado no lote atual; somente demonstração.', 'sales_value', 'MinMaxScaler; constantes 0; ausências preservadas.'),
 'demo_sales_zscore': ('Valor comercializado padronizado no lote atual; somente demonstração.', 'sales_value', 'StandardScaler, variância populacional; constantes 0; ausências preservadas.'),
 'demo_status_delivered': ('Dummy nominal para delivered; somente demonstração.', 'order_status', 'One-hot com categorias fixas.'),
 'demo_status_shipped': ('Dummy nominal para shipped; somente demonstração.', 'order_status', 'One-hot com categorias fixas.'),
 'demo_status_other': ('Dummy nominal para demais status; somente demonstração.', 'order_status', 'One-hot com categorias fixas; inclui desconhecidos.')}


def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_outputs(d, raw, root, charts=True):
    root = Path(root)
    processed, reports = root / 'data/processed', root / 'reports'
    processed.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    if set(FIELD_INFO) != set(d.columns):
        raise ValueError('Dicionário não corresponde ao esquema analítico.')
    path = processed / 'tabela_analitica.csv'
    # Escrita temporária evita substituir uma entrega válida por um arquivo incompleto.
    temp = path.with_suffix('.tmp')
    d.to_csv(temp, index=False, float_format='%.8g')
    if temp.stat().st_size >= 100_000_000:
        temp.unlink()
        raise ValueError('CSV excede 100 MB. Arquivo anterior preservado. Revisar precisão/colunas demonstrativas antes de publicar.')
    temp.replace(path)
    metadata = {'rows': len(d), 'columns': len(d.columns), 'bytes': path.stat().st_size,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'grain': 'order_id + seller_id'}
    (processed / 'metadados.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    audit = d.attrs['audit']
    (reports / 'evidencias.json').write_text(json.dumps(json_safe(audit), ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    selected, corr = selection_report(d)
    (reports / 'selecao_atributos.json').write_text(json.dumps(json_safe(selected), ensure_ascii=False, indent=2), encoding='utf-8')
    corr.to_csv(reports / 'correlacoes.csv', index=True)
    d.describe(include='all').to_csv(reports / 'estatisticas_final.csv')
    for name, frame in zip(REQUIRED, raw):
        numeric = [c for c in frame if c in ['price', 'freight_value', 'review_score'] or c.startswith('product_') and c != 'product_id' and c != 'product_category_name']
        if numeric:
            frame[numeric].apply(pd.to_numeric, errors='coerce').describe().to_csv(reports / f'estatisticas_brutas_{name}.csv')
        pd.DataFrame({'tipo_carregado': frame.dtypes.astype(str), 'nulos': frame.isna().sum(),
            'distintos': frame.nunique()}).to_csv(reports / f'perfil_{name}.csv')
    seller_metrics(d).to_csv(reports / 'metricas_vendedores.csv', index=False)
    review_comparison(d).to_csv(reports / 'comparacao_avaliacoes.csv', index=False)
    e = d[d.eligible_dispatch]
    deadline_comparison = []
    for reference, column in [('menor_prazo', 'shipping_limit_date'), ('maior_prazo', 'shipping_limit_max')]:
        late = e.order_delivered_carrier_date.gt(e[column])
        deadline_comparison.append({'referencia': reference, 'pedidos_elegiveis': len(e),
            'atrasos': int(late.sum()), 'taxa_atraso': late.mean()})
    pd.DataFrame(deadline_comparison).to_csv(reports / 'comparacao_prazos.csv', index=False)
    missing_alternatives = [{'tabela': name, 'unidade': 'linha original', 'preservar_linhas': len(frame),
        'excluir_qualquer_nulo_linhas_restantes': int(frame.notna().all(axis=1).sum()),
        'linhas_que_seriam_removidas': int(frame.isna().any(axis=1).sum())} for name, frame in zip(REQUIRED, raw)]
    pd.DataFrame(missing_alternatives).to_csv(reports / 'alternativas_ausencias.csv', index=False)
    e.groupby('purchase_month').dispatch_late.agg(['mean', 'count', 'sum']).to_csv(reports / 'serie_mensal.csv')
    reviewed = d[d.eligible_review]
    reviewed.groupby(['purchase_month', 'dispatch_late', 'delivery_late'], dropna=False).review_score.agg(['mean', 'count']).to_csv(reports / 'avaliacoes_estratificadas.csv')
    lines = ['# Dicionário de dados - Anexo C', '', 'Uma linha por pedido-vendedor observado. Flags booleanas; dias corridos; valores em BRL.', '',
        '| Coluna | Tipo em memória | Origem | Descrição | Tratamento aplicado |', '|---|---|---|---|---|']
    for c in d:
        desc, origin, treatment = FIELD_INFO[c]
        lines.append(f'| {c} | {d[c].dtype} | {origin} | {desc} | {treatment} |')
    (reports / 'dicionario_de_dados.md').write_text('\n'.join(lines), encoding='utf-8')
    values = e.approval_to_carrier_days
    outliers = e.dispatch_time_outlier.astype(bool)
    alternatives = pd.DataFrame([
        {'alternativa': 'preservar', 'linhas': len(e), 'media_dias': values.mean(), 'taxa_atraso': e.dispatch_late.mean()},
        {'alternativa': 'excluir_outliers', 'linhas': int((~outliers).sum()), 'media_dias': values[~outliers].mean(), 'taxa_atraso': e.loc[~outliers, 'dispatch_late'].mean()},
        {'alternativa': 'limitar_IQR_apenas_demonstracao', 'linhas': len(e), 'media_dias': e.demo_dispatch_clipped.mean(), 'taxa_atraso': e.dispatch_late.mean()}])
    alternatives.to_csv(reports / 'alternativas_outliers.csv', index=False)
    before_after = pd.DataFrame([{'tabela': k, 'linhas_brutas': audit['before'][k]['rows'],
        'duplicatas_exatas': audit['before'][k]['duplicates'], 'linhas_tratadas': audit['after'][k]['rows'],
        'chaves_nulas_removidas': audit['null_keys_removed'][k]} for k in REQUIRED])
    before_after.to_csv(reports / 'antes_depois.csv', index=False)
    diary = reports / 'diario_de_decisoes.md'
    if not diary.exists():
        diary.write_text('''# Diário de decisões - Anexo B

MODELO PARA AUTORIA HUMANA. Evidências geradas automaticamente estão em evidencias.json,
antes_depois.csv, alternativas_outliers.csv e selecao_atributos.json. Preencha com decisões
efetivamente discutidas pela equipe. A implementação técnica atual é uma proposta da ferramenta.
As justificativas não foram geradas por IA. Acrescente linhas para todas as decisões reais.

| Nº | Etapa | Problema encontrado | Decisão tomada | Justificativa (autoria humana) | Impacto nos dados |
|---|---|---|---|---|---|
| 1 | Ausências | Consultar evidencias.json: before/nulls | [Equipe preencher] | [Equipe redigir] | [Equipe citar contagens] |
| 2 | Duplicatas e chaves | Consultar antes_depois.csv | [Equipe preencher] | [Equipe redigir] | [Equipe citar contagens] |
| 3 | Outliers | Consultar alternativas_outliers.csv | [Equipe preencher] | [Equipe redigir] | [Equipe comparar alternativas] |
| 4 | Datas e inconsistências | Consultar invalid_dates e invalid_chronology_pairs | [Equipe preencher] | [Equipe redigir] | [Equipe citar contagens] |
| 5 | Granularidade e avaliações | Consultar reviews_reduced e multi_seller_orders | [Equipe preencher] | [Equipe redigir] | [Equipe citar contagens] |
| 6 | Transformações e seleção | Consultar selecao_atributos.json | [Equipe preencher] | [Equipe redigir] | [Equipe citar atributos] |
''', encoding='utf-8')
    if charts:
        save_charts(d, reports / 'graficos')
    return metadata
