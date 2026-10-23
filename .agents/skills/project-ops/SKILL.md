---
name: project-ops
description: Atualizar estratégia, experimentos e painel do projeto Caixa Leve com evidências e histórico.
---

# Operação do projeto

1. Leia README.md, docs/01-pesquisa.md e o estado ativo em data/state.json (fallback: data/seed.json).
2. Separe evidência observada, hipótese e decisão. Para pesquisa externa, anote URL, data, trecho ou captura e restrições. Se a rede falhar, mantenha a questão pendente.
3. Para atualizar o painel, carregue GET /api/state, preserve campos e revisão e envie PUT /api/state com application/json. Se houver 409, releia e concilie, sem apagar mudanças do usuário. Se o servidor estiver parado, inicie `python server.py` no checkout existente. Não crie worktree sem solicitação.
4. Registre decisões com data e justificativa; altere tarefas e próximos experimentos. Não copie dados pessoais ou segredos para arquivos rastreados.
5. Para avaliar mídia, use a mesma coorte, janela de atribuição e definição de lead/ativação/pagante. Zero clientes torna CAC indefinido. Inclua custos não publicitários na avaliação comercial.
6. Criativos: siga docs/05-criativos-vmake.md. Não simule cliente real, testemunho, faturamento ou produto já disponível. Use imagens e voz com direitos de uso.
7. Código: rode `python -m unittest discover -s tests -v` e `node --check web/app.js`. Documente mudanças e publique no GitHub somente dentro do escopo solicitado. Gasto, campanha ao vivo e comunicações externas exigem instrução explícita.

Esta skill foi criada para este repositório. Não instala ferramentas externas nem conecta este chat a serviços por conta própria.
