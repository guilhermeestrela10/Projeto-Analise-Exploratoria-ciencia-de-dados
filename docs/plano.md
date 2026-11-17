# Implementação - Grupo 04

Referências: pedido fornecido pelo usuário e PDF FINAL BOSS, 12 páginas, lido integralmente em 17/11/2026.
Pasta inicialmente vazia. Implementação direta autorizada pelo usuário, sem aprovação intermediária.

## Arquitetura e escopo
Python, Pandas, NumPy, Scikit-Learn somente para pré-processamento, Matplotlib, Seaborn e Streamlit.
Cinco arquivos Olist; geolocalização excluída. Uma linha por pedido-vendedor, com agregação dos itens antes dos merges.
A análise principal usa somente pedidos com um vendedor observado. Em recortes incompletos isso não comprova vendedor único no universo original.
Não há registro de despacho por vendedor: a data do pedido é uma aproximação, inclusive em pedidos com vendedor único.
Avaliações reduzidas a uma por pedido por regra determinística. Nenhum texto livre de cliente será publicado.
Preservar dados originais. Marcar ausências, inconsistências e outliers; não imputar datas, notas ou indicadores de atraso.
Campos demonstrativos de codificação, MinMax e Z-score separados das medidas gerenciais.

## Etapas e verificações
- [x] Testes de contrato: granularidade, múltiplos vendedores, nulos, datas inválidas, amostras vazias e constantes, chaves conflitantes.
- [x] src/load_data.py, preprocessing.py e feature_engineering.py: carga, validação e preprocessar(orders, items, products, sellers, reviews).
- [x] src/analysis.py e visualizations.py: denominadores explícitos, agregações filtradas, correlações, EDA, gráficos.
- [x] scripts/executar_pipeline.py: CSV, evidências, dicionário completo, relatórios e hashes dos arquivos.
- [x] app.py, pages/ e src/dashboard.py: quatro páginas, período e estado, mínimo de volume, vazio e conclusões humanas externas.
- [x] Testes Streamlit AppTest e teste integrado com recorte real preservando relacionamentos.
- [x] Notebook executado, PDF técnico revisado visualmente, documentação, apresentação e auditoria da rubrica.
- [x] Revisar comandos, tamanho do CSV, dependências e publicação possível sem inventar links ou autoria.

## Autoria
Justificativas do diário, sumário executivo, respostas de negócio e conclusões ficam vazios e identificados para autoria humana (PDF, seção 7.1).
Registros técnicos produzidos automaticamente não representam decisões validadas pela equipe. Nenhum commit de integrante será simulado.

## Resultado da execução

25 testes passaram; CSV real de 38.373.468 bytes e 41 colunas. Evidências completas em reports/verificacao.md.
Publicação e autoria humana permanecem pendentes e estão documentadas; nenhum commit ou remoto foi criado.
