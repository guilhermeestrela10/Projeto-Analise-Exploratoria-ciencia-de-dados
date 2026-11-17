# Respostas fornecidas pelo solicitante

Transcrição das respostas recebidas nesta conversa. A revisão abaixo não comprova validação dos demais integrantes.

## Texto recebido

1. Onde está o problema do atraso no despacho? O atraso está concentrado em uma cauda longa de parceiros específicos (cerca de 10% a 15% dos vendedores), que demoram mais do que o prazo limite (shipping_limit_date) para entregar o pacote à transportadora.

2. Vendedores que atrasam recebem avaliações piores? Sim, existe uma correlação direta e forte: pedidos com atrasos no despacho ou na entrega apresentam uma concentração expressiva de notas 1 e 2, prejudicando a reputação da Olist perante o consumidor.

3. Que critérios objetivos a empresa pode usar para acompanhar os vendedores? A adoção de três métricas automáticas: a Taxa de Atraso de Despacho (TAD) superior a 10%, a Nota Média Ponderada nos últimos 30 dias (piso de 3.8) e o Tempo Médio de Postagem em dias úteis.

## Conferência técnica da ferramenta

- A primeira pergunta oficial é “Quais vendedores mais atrasam o despacho dos pedidos?”. O texto recebido não identifica os vendedores. O ranking e seus denominadores estão em metricas_vendedores.csv.
- O percentual de 10% a 15% dos vendedores não foi demonstrado pelo texto recebido. Falta definir concentração de quê, denominador e recorte.
- A comparação de pedidos elegíveis apresenta médias 4,1939 sem atraso e 3,6820 com atraso. Notas negativas: 11,8896% e 24,2120%, respectivamente.
- Pearson entre atraso binário e nota: -0,1143. Entre taxa de atraso e nota média de vendedores com ao menos 30 pedidos elegíveis: -0,4706. Não sustenta chamar indistintamente a correlação de direta e forte, nem comprova causalidade.
- A terceira resposta propõe TAD > 10%, piso de nota 3,8 e tempo em dias úteis. Esses são critérios propostos pelo solicitante, não limites inferidos automaticamente como uma política comprovada.
- “Nota ponderada” precisa de pesos definidos. Também é necessário definir a data de referência dos últimos 30 dias e o calendário de dias úteis. Os dados Olist são históricos; usar a data atual de 2026 produziria uma janela sem pedidos.

As respostas serão integradas preservando o texto original e destacando as validações pendentes. O diário ainda precisa das decisões e justificativas reais do grupo.
