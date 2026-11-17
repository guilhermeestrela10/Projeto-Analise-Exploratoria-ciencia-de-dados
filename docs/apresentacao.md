# Guia de estudo e demonstração - 02/12/2026

Material técnico assistido por IA. Não contém respostas de negócio nem conclusões da equipe.
Cada integrante deve executar o pipeline e entender qualquer função; a professora pode escolher quem responde.

## Arquitetura em uma leitura

Cinco CSVs originais -> load_data -> preprocessar -> validação e limpeza -> itens agregados por pedido-vendedor
-> dimensões e avaliação única -> engineer -> CSV final -> indicadores e páginas Streamlit.
Somente o CSV final alimenta os dados do painel. O notebook chama as mesmas funções.

## Funções e merges

- `load_data(folder)`: valida os cinco nomes e carrega textos preservando identificadores.
- `preprocessar(orders, items, products, sellers, reviews)`: copia entradas, valida colunas/chaves, converte tipos, agrega e retorna a tabela final.
- `engineer(d)`: calcula diferenças temporais, flags, extração de mês/dia, razões, clipping demonstrativo e escalas.
- `seller_metrics(d)`: agrega novamente o recorte atual, calcula taxas e intervalos de Wilson.
- `review_comparison(d)`: compara notas dos pedidos elegíveis com e sem atraso.
- `write_outputs(d, raw, root)`: salva CSV, tamanho/hash, perfis, estatísticas, gráficos e dicionário.
- Merges: itens-produtos N:1; grupos-contagens N:1; grupos-pedidos N:1; grupos-vendedores N:1; grupos-avaliação única N:1.
- Se juntar avaliações diretamente aos itens, uma nota pode aparecer várias vezes. Por isso primeiro se agregam itens e se seleciona uma avaliação por pedido.

## Indicadores para explicar com palavras próprias

Taxa de atraso: pedidos elegíveis com despacho após o prazo / todos os pedidos elegíveis.
Excesso médio: média de max(despacho - prazo, 0), incluindo zero nos pedidos em prazo.
Nota média: notas válidas dos pedidos elegíveis, uma por pedido.
Percentual negativo: notas 1 ou 2 / notas válidas.
Intervalo de Wilson: faixa descritiva de incerteza da taxa; poucos pedidos produzem faixas maiores.
Outlier pelo IQR: ponto fora das cercas; não é automaticamente erro.
MinMax: leva o menor valor a 0 e o maior a 1. Z-score: centraliza na média e divide pelo desvio padrão populacional.
Constantes viram zero; ausências continuam ausentes; escalas dependem do lote.

## Roteiro de até 10 minutos

| Tempo | Atividade a ensaiar |
|---|---|
| 0:00-0:40 | Abrir painel publicado e apresentar briefing; texto produzido pela equipe |
| 0:40-2:00 | Página de atrasos: escolher período/UF, explicar volume e denominador; resposta humana |
| 2:00-3:30 | Página de avaliações: comparar grupos e reconhecer ausência de causalidade; interpretação humana |
| 3:30-5:00 | Página de critérios: mostrar cenário e critérios que a equipe de fato escolheu e justificou |
| 5:00-5:40 | Mostrar cinco arquivos brutos recebidos e cabeçalhos |
| 5:40-7:00 | Executar comando de amostra abaixo; abrir CSV e evidências geradas |
| 7:00-8:00 | Explicar merges, unidade pedido-vendedor e seleção de avaliação |
| 8:00-9:00 | Integrantes explicam uma decisão real do diário e seu impacto |
| 9:00-10:00 | Mostrar um teste relevante e explicar limitações e registro de IA |

## Comandos para ensaio

```powershell
.\.venv\Scripts\python.exe scripts/executar_pipeline.py --input data/amostra_bruta --output work/demonstracao --sem-graficos
.\.venv\Scripts\python.exe -m streamlit run app.py
.\.venv\Scripts\python.exe -m pytest tests/test_preprocessing.py -q
```

Antes da demonstração: manter o ambiente instalado; verificar os cinco CSVs e abrir um terminal na raiz.
O comando de amostra não modifica a base do painel. Para usar outra base no painel, gerar conscientemente na raiz com `--output .`.

## Perguntas técnicas para estudar

1. Qual a chave de cada tabela? Qual a chave final? Por que um pedido aparece em mais de uma linha?
2. Por que a data de transportadora não identifica o despacho de cada vendedor?
3. O que acontece quando uma amostra omite um vendedor do pedido?
4. Por que uma nota não pode ser contada várias vezes após um merge?
5. O que diferencia ausência de data de um atraso igual a zero?
6. Como é escolhido o prazo se existem vários itens? Qual impacto de usar o maior prazo?
7. Por que preservar um atraso extremo? O que muda se ele for removido?
8. Como o programa se comporta com um pedido, nenhuma categoria ou nenhuma correspondência?
9. Por que as escalas não são usadas para mostrar dias e BRL ao gestor?
10. Como demonstrar que um filtro alterou tanto o gráfico quanto o denominador?
11. Por que correlação e comparação de grupos não demonstram causalidade?
12. Qual decisão a equipe mudou após analisar os dados? Onde está sua justificativa humana?
13. Qual sugestão automática foi inadequada e como o grupo percebeu isso? Não inventar revisão que não ocorreu.

## Pendências de estudo

Escrever respostas de negócio, justificar decisões, validar os parâmetros do cenário, confirmar responsáveis,
revisar código e produzir contribuições reais. Ensaiar a amostra nova, não somente a base completa.
