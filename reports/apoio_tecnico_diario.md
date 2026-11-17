# Apoio técnico para estudar o diário

Material automático, registro 5. Não é o diário final e não documenta discussões que o grupo tenha realizado.
Os integrantes devem explicar, com suas próprias palavras, as decisões que realmente avaliaram e escolheram.

## Unidade de observação

A data de transportadora e a avaliação pertencem ao pedido inteiro. Quando há vários vendedores,
a base não informa qual deles causou o atraso ou a nota. O código mantém essas linhas, mas não as usa
na comparação individual principal. Isso reduz a amostra e limita a abrangência dos resultados.

## Ausência não é atraso zero

Sem data de despacho não existe duração observada. Sem avaliação não existe nota observada.
Preencher esses campos com zero ou média alteraria os denominadores e poderia fabricar pontualidade
ou satisfação. O pipeline sinaliza a ausência e calcula cada indicador somente nos registros elegíveis.

## Extremos

Um atraso muito grande pode ser um problema operacional real. O IQR identifica pontos extremos,
mas não comprova que sejam erros. A comparação gerada mostra 94.955 pedidos elegíveis preservados,
contra 89.564 se os extremos fossem removidos; a taxa observada mudaria de 9,2349% para 5,6585%.
O código mantém os valores originais e limita valores somente em uma coluna demonstrativa.

## Menor prazo

Um pedido-vendedor pode ter itens com prazos distintos. Comparar o despacho com o menor prazo
identifica se ao menos um dos compromissos foi ultrapassado; usar o maior prazo produz uma medida menos restritiva.
A comparação de sensibilidade está em comparacao_prazos.csv. Nenhuma dessas aproximações recupera despachos por item que a base não fornece.

## Limites escolhidos pelo solicitante

TAD > 10% e nota < 3,8 foram propostos pelo solicitante, não descobertos como limites ótimos nos dados.
O acompanhamento utiliza volume, nota e tempo para apoiar avaliação humana. O código não dispara
advertências nem comprova a eficácia desses parâmetros. A janela histórica e o calendário foram explicitamente aprovados pelo solicitante.

Para transformar este estudo em diário, os integrantes precisam dizer quais alternativas consideraram,
quais realmente adotaram e sua própria justificativa. Não apresentar este material como texto autoral da equipe.
