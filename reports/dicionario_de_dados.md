# Dicionário de dados - Anexo C

Uma linha por pedido-vendedor observado. Flags booleanas; dias corridos; valores em BRL.

| Coluna | Tipo em memória | Origem | Descrição | Tratamento aplicado |
|---|---|---|---|---|
| order_id | string | orders.order_id / items.order_id | Identificador do pedido; parte da chave final. | Texto sem espaços; chave validada. |
| seller_id | string | items.seller_id | Identificador do vendedor observado; parte da chave final; pode ser desconhecido. | Texto sem espaços; ausências preservadas em grupo próprio e excluídas da comparação individual. |
| item_count | int64 | items.order_item_id | Quantidade de itens do vendedor neste pedido. | Contagem após remoção de duplicatas exatas. |
| sales_value | float64 | items.price | Valor dos itens deste vendedor no pedido, em BRL; não é receita líquida. | Soma completa; grupo com valor inválido fica ausente. |
| freight_value | float64 | items.freight_value | Frete dos itens deste vendedor no pedido, em BRL. | Soma completa; negativos e inválidos viram ausência. |
| shipping_limit_date | datetime64[ns] | items.shipping_limit_date | Menor prazo de despacho dos itens deste vendedor. | Conversão segura e mínimo por pedido-vendedor. |
| shipping_limit_max | datetime64[ns] | items.shipping_limit_date | Maior prazo de despacho dos itens deste vendedor. | Conversão segura e máximo por pedido-vendedor. |
| deadlines_complete | bool | items.shipping_limit_date | Todos os itens do grupo possuem prazo válido. | Indicador booleano; requisito de elegibilidade. |
| category_count | int64 | products.product_category_name | Número de categorias observadas no grupo. | Contagem distinta, incluindo sem_categoria. |
| category_main | string | items.product_id / products.product_category_name | Categoria mais frequente no grupo; não representa todos os itens. | Texto minúsculo; ausências sem_categoria; empate alfabético. |
| seller_count | int64 | items.seller_id | Número de vendedores distintos observados no pedido, incluindo grupo desconhecido. | Contagem inclui ausência para impedir falsa identificação de vendedor único; depende da cobertura da amostra. |
| order_item_count | int64 | items.order_item_id | Quantidade total de itens observados no pedido. | Contagem por pedido; repetida em cada vendedor, não somar entre vendedores. |
| order_status | string | orders.order_status | Situação do pedido. | Minúsculo, espaços externos removidos, ausência unknown. |
| order_purchase_timestamp | datetime64[ns] | orders.order_purchase_timestamp | Data e hora da compra; filtro temporal. | to_datetime errors=coerce; sem imputação. |
| order_approved_at | datetime64[ns] | orders.order_approved_at | Data e hora da aprovação. | Conversão segura; sem imputação. |
| order_delivered_carrier_date | datetime64[ns] | orders.order_delivered_carrier_date | Data de entrega à transportadora do pedido, sem detalhe por vendedor. | Conversão segura; aproximação do despacho individual. |
| order_delivered_customer_date | datetime64[ns] | orders.order_delivered_customer_date | Data de entrega ao cliente. | Conversão segura; sem imputação. |
| order_estimated_delivery_date | datetime64[ns] | orders.order_estimated_delivery_date | Dia previsto para entrega ao cliente. | Conversão segura; comparação por dia civil. |
| seller_state | string | sellers.seller_state | UF do vendedor. | Maiúsculas; UF inválida ou dimensão ausente SEM_INFORMACAO. |
| review_score | float64 | reviews.review_score / review_answer_timestamp / review_id | Nota inteira de 1 a 5, única por pedido; repetida em pedidos multivendedor. | Última resposta datada; empates por ID, nota e tamanho; fora de 1..5 ausente. |
| review_text_length | float64 | reviews.review_comment_message | Comprimento do comentário selecionado após limpeza; sem publicar texto livre. | NFKC, minúsculas, espaços simples; ausência vira comprimento 0; não mede sentimento. |
| invalid_chronology | bool | Datas de compra, aprovação, despacho, prazo e entrega | Alguma sequência temporal observada é contraditória. | Sinalizar; cada duração aplica sua própria elegibilidade. |
| approval_to_carrier_days | float64 | order_delivered_carrier_date - order_approved_at | Dias corridos entre aprovação e transportadora. | Segundos / 86400; exige compra <= aprovação <= despacho. |
| dispatch_delay_days | float64 | order_delivered_carrier_date - shipping_limit_date | Dias corridos de excesso sobre o menor prazo; negativos representam antecedência. | Exige datas coerentes, prazos completos e status delivered/shipped. |
| dispatch_late | Int64 | dispatch_delay_days | 1 para despacho após o prazo, 0 em prazo, ausente se não mensurável. | Comparação estrita > 0; não imputar ausência como zero. |
| eligible_dispatch | bool | seller_count / datas / deadlines_complete / order_status | Pedido elegível à comparação individual de despacho. | Um vendedor observado; datas completas e coerentes; delivered ou shipped. |
| transport_days | float64 | order_delivered_customer_date - order_delivered_carrier_date | Dias entre transportadora e cliente. | Segundos / 86400; somente sequência não negativa. |
| delivery_days | float64 | order_delivered_customer_date - order_purchase_timestamp | Dias entre compra e entrega ao cliente. | Segundos / 86400; somente sequência não negativa. |
| delivery_late | Int64 | order_delivered_customer_date / order_estimated_delivery_date | 1 se entregue depois do dia prometido; ausente se não mensurável. | Datas normalizadas; entrega no mesmo dia não é atraso. |
| negative_review | Int64 | review_score | 1 para nota 1 ou 2; 0 para 3 a 5; ausência preservada. | Indicador nullable; não é análise de sentimento. |
| eligible_review | bool | eligible_dispatch / review_score | Elegível para comparar notas e atraso individual de despacho. | Despacho elegível e nota válida disponível. |
| purchase_month | string | order_purchase_timestamp | Mês da compra, AAAA-MM. | Extração temporal; sem imputação. |
| purchase_weekday | Int64 | order_purchase_timestamp | Dia da semana da compra: segunda 0, domingo 6. | Extração temporal nullable. |
| freight_share | float64 | freight_value / (sales_value + freight_value) | Fração do frete no valor de itens mais frete. | Denominador positivo; fração 0..1, não percentual monetário adicional. |
| dispatch_time_outlier | bool | approval_to_carrier_days / eligible_dispatch | Tempo de despacho fora das cercas IQR dos pedidos elegíveis do lote. | Q1-1.5 IQR e Q3+1.5 IQR; não exclui linhas. |
| demo_dispatch_clipped | float64 | approval_to_carrier_days | Tempo de despacho limitado às cercas IQR; somente demonstração. | Clipping; medida original preservada e usada nos indicadores. |
| demo_sales_minmax | float64 | sales_value | Valor comercializado normalizado no lote atual; somente demonstração. | MinMaxScaler; constantes 0; ausências preservadas. |
| demo_sales_zscore | float64 | sales_value | Valor comercializado padronizado no lote atual; somente demonstração. | StandardScaler, variância populacional; constantes 0; ausências preservadas. |
| demo_status_delivered | int64 | order_status | Dummy nominal para delivered; somente demonstração. | One-hot com categorias fixas. |
| demo_status_shipped | int64 | order_status | Dummy nominal para shipped; somente demonstração. | One-hot com categorias fixas. |
| demo_status_other | int64 | order_status | Dummy nominal para demais status; somente demonstração. | One-hot com categorias fixas; inclui desconhecidos. |