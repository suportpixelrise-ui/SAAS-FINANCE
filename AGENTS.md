# Instruções do projeto

Leia README.md e docs/ antes de alterar estratégia. Use a skill local `.agents/skills/project-ops/SKILL.md` para gestão do projeto. Trabalhe no checkout existente; não crie worktrees sem solicitação.

Não trate hipóteses como resultados de mercado. Registre fonte, data e evidência para novas afirmações. Não invente preços concorrentes, depoimentos, ganhos de tempo ou performance de anúncios. Leia data/state.json se existir; caso contrário data/seed.json. Atualizações do estado devem usar GET/PUT /api/state, incluindo revisão, ou edição cuidadosa com o servidor parado. Não publique o estado privado no Git.

Alterações de código: execute testes existentes e verificação JavaScript. Não anuncie publicação, integração, pagamento ou geração de vídeo sem execução comprovada. A autorização para estruturar o projeto não autoriza gastar verba, veicular anúncios ou contratar serviços.

## Painel Netlify (versão atual)
A interface é estática e usa localStorage; a API Python não atualiza os dados do navegador. Leia o ZIP exportado pelo usuário para conhecer o estado atual. Devolva project.json validado em ZIP_STORED para importação, ou gere site com scripts/package_netlify.py. Nunca inclua dados privados em site público. A atualização de site mantém localStorage; o usuário aplica o plano incluído pelo botão específico. Consulte README.md.
