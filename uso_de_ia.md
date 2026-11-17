# Registro de uso de IA - Anexo D

Data desta implementação: 17/11/2026. Ferramenta: Codex, nesta conversa.
Os registros descrevem assistência automática solicitada; não comprovam revisão nem participação dos demais integrantes.
O usuário deve confirmar sua identificação como integrante solicitante e fornecer o link compartilhável da conversa, se disponível.

| Nº | Data | Integrante | Ferramenta | Etapa e o que foi pedido | O que foi aproveitado | O que a equipe alterou ou verificou | Link da conversa |
|---|---|---|---|---|---|---|---|
| 1 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Implementar limpeza, testes e feature engineering | src/preprocessing.py, src/feature_engineering.py, testes correspondentes | Revisão humana pendente; verificações automáticas em reports/verificacao.md | Pendente, caso a ferramenta permita |
| 2 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Análises, gráficos, painel e testes | src/analysis.py, src/visualizations.py, src/dashboard.py, app.py, pages/, testes | Revisão humana pendente; verificar métricas, limites e interpretações | Pendente |
| 3 | 17/11/2026 | Solicitante desta conversa; confirmar nome | Codex | Carga, aquisição, pipeline, notebook e documentação técnica | src/load_data.py, src/reporting.py, scripts/, notebook, documentos técnicos | Revisão humana pendente; conferir evidências da execução automática | Pendente |

## Limites de autoria
O PDF, seção 7.1, proíbe IA nas justificativas do diário, sumário executivo, respostas de negócio e conclusões.
Esses textos não foram gerados. Campos vazios precisam ser escritos pela equipe. Evidências e descrições técnicas automáticas estão identificadas.
As regras de limpeza e métricas implementadas são propostas técnicas da ferramenta, ainda sujeitas à avaliação dos integrantes.
Não registrar revisão humana antes de realizá-la. Não atribuir decisões automáticas aos estudantes.
Todo arquivo Python gerado recebe a marcação de registro; o marcador no início abrange o arquivo inteiro.
Commits futuros que contenham código assistido devem incluir [IA]. Não foram criados commits em nome de integrantes.

## Verificação e erros da ferramenta
Consultar reports/verificacao.md para comandos efetivamente executados, falhas e correções observadas.
Na leitura inicial do PDF houve UnicodeEncodeError no terminal Windows; a leitura integral foi repetida com python -X utf8.
O registro de correções automáticas não substitui o exemplo crítico e a explicação que cada integrante deve conseguir apresentar.
