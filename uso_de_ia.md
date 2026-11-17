# Registro de uso de IA - Anexo D

Data desta implementação: 17/11/2026. Ferramenta: Codex, nesta conversa.
Os registros descrevem assistência automática solicitada; não comprovam revisão nem participação dos demais integrantes.
O usuário deve confirmar sua identificação como integrante solicitante e fornecer o link compartilhável da conversa, se disponível.

| Nº | Data | Integrante | Ferramenta | Etapa e o que foi pedido | O que foi aproveitado | O que a equipe alterou ou verificou | Link da conversa |
|---|---|---|---|---|---|---|---|
| 1 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Implementar limpeza, testes e feature engineering | src/preprocessing.py, src/feature_engineering.py, testes correspondentes | Revisão humana pendente; verificações automáticas em reports/verificacao.md | Pendente, caso a ferramenta permita |
| 2 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Análises, gráficos, painel e testes | src/analysis.py, src/visualizations.py, src/dashboard.py, app.py, pages/, testes | Revisão humana pendente; verificar métricas, limites e interpretações | Pendente |
| 3 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Carga, aquisição, pipeline, notebook e documentação técnica | src/load_data.py, src/reporting.py, scripts/, notebook, documentos técnicos | Revisão humana pendente; conferir evidências da execução automática | Pendente |
| 4 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Revisar contra o PDF, preparar publicação e apontar pendências de entrega | Correção da contagem de notas inválidas, teste de regressão, verificar_entrega.py, testes e workflow GitHub Actions | Verificações automáticas registradas em docs/revisao_final.md; autoria e revisão humana continuam pendentes | Pendente |
| 5 | 17/11/2026 | Solicitante desta conversa | Codex | Integrar três respostas fornecidas, corrigir afirmações e implementar critérios definidos pelo solicitante | Textos originais preservados em reports/respostas_recebidas.md; revisão factual autorizada; limites TAD 10%, nota 3,8, janela de 30 dias e dias úteis sem feriados | O solicitante autorizou expressamente as correções factuais e as definições da janela e pesos; não confirmou revisão de todo o código nem justificativas reais do grupo | Pendente |

## Limites de autoria
O PDF, seção 7.1, proíbe IA nas justificativas do diário, sumário executivo, respostas de negócio e conclusões.
Esses textos não foram gerados. Campos vazios precisam ser escritos pela equipe. Evidências e descrições técnicas automáticas estão identificadas.
As regras de limpeza e métricas implementadas são propostas técnicas da ferramenta, ainda sujeitas à avaliação dos integrantes.
Não registrar revisão humana antes de realizá-la. Não atribuir decisões automáticas aos estudantes.
Todo arquivo Python gerado recebe a marcação de registro; o marcador no início abrange o arquivo inteiro.
Commits futuros que contenham código assistido devem incluir [IA]. Não foram criados commits em nome de integrantes.

Na segunda revisão foi encontrado o commit local preexistente `45ad1cf` (mensagem `salvando`),
criado pelo proprietário entre as sessões. Ele foi preservado, sem reescrever sua autoria ou mensagem.
As alterações assistidas desta revisão serão identificadas nos novos commits com [IA].

## Verificação e erros da ferramenta
Consultar reports/verificacao.md para comandos efetivamente executados, falhas e correções observadas.
Na leitura inicial do PDF houve UnicodeEncodeError no terminal Windows; a leitura integral foi repetida com python -X utf8.
O registro de correções automáticas não substitui o exemplo crítico e a explicação que cada integrante deve conseguir apresentar.
