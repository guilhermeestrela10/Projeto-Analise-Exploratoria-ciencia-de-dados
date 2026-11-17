# Publicação e entrega

## GitHub

Nome solicitado: `Projeto-Analise-Exploratoria-Grupo04`. Visibilidade pública.
Antes de publicar, conferir `uso_de_ia.md`, autoria humana e arquivos selecionados.
Versionar código, notebook, requirements.txt, documentação, CSV final, metadados e relatório após preenchimento.
Não versionar `.venv`, dados brutos, textos livres de avaliações, credenciais, caches ou work/.
O PDF oficial é referência da disciplina; não é necessário redistribuí-lo em repositório público.

Se o repositório ainda não existir, criar na conta do proprietário pelo GitHub e seguir os comandos exibidos lá.
Antes do primeiro commit, executar `git status --short` e conferir o que será incluído.
Usar mensagens com `[IA]` quando houver código assistido. Cada integrante deve fazer sua própria contribuição real.
Não compartilhar credenciais nem simular commits dos colegas.

O Git local já está inicializado na branch `main`, sem commits e sem remoto. Após a revisão humana,
o proprietário pode executar na raiz (os comandos abaixo ainda não foram executados):

```powershell
gh auth login
gh auth setup-git
git add .
git diff --cached --stat
git commit -m "feat: projeto Olist Grupo04 [IA]"
gh repo create Projeto-Analise-Exploratoria-Grupo04 --public --source=. --remote=origin --push
```

Conferir o conteúdo staged antes do commit: somente os arquivos listados na auditoria devem entrar.
Se o repositório já tiver sido criado pela equipe, usar seu endereço real com `git remote add origin`
e publicar com `git push -u origin main`; não recriar outro repositório.
O CSV final ultrapassa o limite comum de upload pelo navegador; usar Git para enviar o arquivo de 38,37 MB.

## Streamlit Community Cloud

1. Entrar com a conta autorizada em https://share.streamlit.io/.
2. Conectar o repositório público e selecionar a branch publicada.
3. Arquivo principal: `app.py`. Versão Python: `3.11` nas configurações avançadas.
4. Manter `requirements.txt` na raiz e `data/processed/tabela_analitica.csv` versionado.
5. Não executar download nem pipeline na inicialização do painel; os dados já devem estar no CSV final.
6. Abrir o link publicado em janela anônima. Visitar quatro páginas e testar UF, vendedor, período e recorte vazio.
7. Inserir links reais no README e manter o painel acessível até a apresentação de 02/12/2026.

## Relatório e envio

O PDF técnico gerado tem indicação de rascunho. A equipe precisa escrever a Parte A,
justificativas da Parte C, respostas do painel e conclusão técnica autoral antes da entrega.
Completar `reports/secoes_autorais.md`, `reports/diario_de_decisoes.md` e `reports/conclusoes_equipe.json`.
Gerar novamente o PDF e revisar todas as páginas. A ferramenta incorpora os arquivos humanos existentes.
Na plataforma A da disciplina, enviar PDF, link GitHub e link Streamlit até **30/11/2026, 23h59 de Brasília**.

Não há links fictícios. O estado efetivamente verificado de autenticação/publicação fica em `reports/verificacao.md`.

Referências verificadas: [GitHub CLI - criar repositório](https://cli.github.com/manual/gh_repo_create), [limites de arquivos no GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) e [deploy no Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app).
