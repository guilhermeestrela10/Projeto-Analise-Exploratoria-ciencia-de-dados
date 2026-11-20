# Guia de estudo e demonstração - 02/12/2026

Roteiro de apoio assistido por IA, registro 8. Responsável pela organização das etapas 7 e 8: Guilherme Estrela.
As respostas integradas estão no painel e no relatório. O solicitante informou revisão do grupo em 18/11/2026.
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
| 0:00-0:40 | Abrir painel publicado e apresentar o problema: monitorar prazos e avaliações dos parceiros |
| 0:40-2:00 | Página de atrasos: aplicar UF/período, explicar denominador e volume mínimo do ranking |
| 2:00-3:30 | Página de avaliações: comparar grupos e explicar que associação não demonstra causalidade |
| 3:30-5:00 | Página de critérios: mostrar janela histórica de 30 dias, TAD > 10%, nota < 3,8 e simulador |
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
Para ensaiar no computador desta revisão, substituir `data/amostra_bruta` por `work/amostra_bruta`.
A amostra local contém 50 pedidos e os registros relacionados das outras quatro tabelas.

## Fala de apoio de Guilherme - etapas 7 e 8

Usar este texto como apoio e explicar as ações enquanto mostra a tela. Os tempos acima são do grupo inteiro;
a distribuição das falas deve ser combinada no ensaio, sem ultrapassar cinco minutos de negócio e cinco de técnica.

“Na etapa 7, minha responsabilidade é o painel Streamlit. Ele tem uma visão geral e três páginas, uma para cada
pergunta do briefing. Os filtros de estado, vendedor e período atualizam os indicadores, as tabelas e os gráficos.
Vou selecionar um estado para mostrar como muda a quantidade de pedidos. Na página de atrasos, o mínimo de
pedidos controla somente o ranking: esse controle evita comparar vendedores com volumes muito diferentes sem olhar a amostra.

Na comparação de avaliações, usamos uma nota por pedido elegível. Na base completa, a média é aproximadamente
4,19 para despachos em prazo e 3,68 para despachos com atraso. Isso mostra uma associação; não prova que o atraso
do vendedor causou a nota menor. Se eu aplicar filtros, esses números são recalculados para o recorte selecionado.

Na terceira página, acompanhamos TAD acima de 10%, nota abaixo de 3,8 e tempo médio em dias úteis. Os últimos
30 dias são contados até a última compra do recorte histórico. O simulador permite discutir volume e limiar;
ele não envia advertências e não substitui a análise dos registros.

Na etapa 8, reuni o relatório, o diário, o dicionário e as instruções no README. Também conferi a integração
do painel com a base final e o teste do pipeline usando uma amostra bruta. Agora vou mostrar onde ficam esses
arquivos e como reproduzir a execução sem alterar a base publicada.”

O texto descreve a responsabilidade atribuída a Guilherme e os recursos disponíveis. A origem da assistência
está em `uso_de_ia.md`; a fala não atribui a Guilherme a implementação individual das etapas anteriores.

## Demonstração guiada do painel

1. Abrir a visão geral e apontar os quatro indicadores. Mostrar o período histórico completo antes de comparar números do relatório.
2. Selecionar UF `PI`. Conferir que “Pedidos no recorte” e os gráficos mudaram. Limpar a seleção antes de continuar.
3. Abrir “Atrasos no despacho”. Mostrar o volume mínimo padrão de 30 pedidos e a tabela abaixo do gráfico.
4. Abrir “Atrasos e avaliações”. Comparar os grupos e seus denominadores; apontar a limitação de causalidade.
5. Abrir “Critérios de acompanhamento”. Mostrar as datas da janela, os critérios e o simulador.
6. Baixar o recorte CSV. Explicar que ele corresponde aos filtros atuais.
7. Na parte técnica, executar o pipeline com os cinco CSVs da amostra e abrir o CSV em `work/demonstracao/data/processed/`.

## Arquivos a deixar abertos antes da apresentação

- Painel publicado e terminal PowerShell na raiz do projeto.
- `reports/relatorio_final.pdf` e `reports/dicionario_de_dados.md`.
- `reports/diario_de_decisoes.md` e `src/preprocessing.py`.
- A pasta com os cinco CSVs brutos da demonstração e o comando com o caminho correto.

Não usar os números da base completa como resposta a um recorte filtrado.
Se a rede falhar, o mesmo painel pode ser aberto localmente com o comando Streamlit acima.

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

## Ensaio da equipe

Combinar a divisão das falas, explicar as decisões documentadas e ensaiar a amostra nova, não somente a base completa.
Cada integrante deve compreender a integração; a revisão informada do relatório não substitui esse preparo.
