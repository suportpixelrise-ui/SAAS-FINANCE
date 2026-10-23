# Caixa Leve — painel estático para Netlify

## Baixar e publicar sem instalar programas

O arquivo [downloads/caixa-leve-netlify.zip](downloads/caixa-leve-netlify.zip) contém o site pronto, sem backend ou build.

1. Baixe e extraia o ZIP.
2. Entre em https://app.netlify.com/drop e envie a pasta extraída que contém `index.html`.
3. Abra o endereço criado pelo Netlify.
4. Para futuras versões, entre no **mesmo site**, na seção de deploys, e envie a nova pasta. Não crie outro site, pois o armazenamento do navegador é separado por endereço.

## Trocar dados com o ChatGPT

- Na aba **Trocar dados com ChatGPT**, escolha **Baixar dados para enviar**. Anexe o ZIP à conversa e descreva o que quer alterar. O ZIP inclui os dados atuais, mesmo com alterações ainda não salvas.
- O assistente pode devolver um ZIP de dados contendo `project.json`, sem compressão (`ZIP_STORED`). Use **Importar ZIP ou JSON atualizado**. Há validação, resumo e confirmação; um backup da tela anterior é baixado antes de aplicar a substituição. Não é uma mesclagem automática.
- Se receber um ZIP do site inteiro atualizado, publique no mesmo site. Os dados já salvos permanecem; use **Revisar e aplicar dados deste ZIP do site** para substituir pelo plano incluído, caso desejado.
- ZIPs comprimidos de outras ferramentas podem precisar ser extraídos para importar apenas `project.json`. Pacotes exportados pelo painel são aceitos diretamente.

Dados ficam no `localStorage` do navegador. Não há login, banco remoto ou comunicação automática com o ChatGPT. Limpar o navegador apaga a cópia local; outro dispositivo exige importar o backup. Dados editados não são enviados ao Netlify, mas qualquer arquivo dentro do ZIP publicado é público. Não publique dados privados no pacote; use apenas o plano público inicial e importe dados pelo painel depois.

## Desenvolvimento e pacotes

```sh
python scripts/package_netlify.py
# Só use --state com dados que podem ser públicos:
python scripts/package_netlify.py --state caminho/plano-publico.json --output artifacts/nova-versao.zip
python server.py
```

Python 3.12+, sem dependências de produção. O servidor local mantém API legada para compatibilidade; a interface atual usa apenas armazenamento do navegador e plano público `data/seed.json`. `data/state.json` da versão antiga não é importado automaticamente: use o JSON pela aba de transferência.

```sh
python -m unittest discover -s tests -v
node --check web/app.js
node --check web/zip.js
# Teste real de navegador, requer Playwright instalado:
python tests/browser_netlify.py
```

Skill do projeto: `.agents/skills/project-ops/SKILL.md`. Não publicar dados privados em commits ou no ZIP. Novas versões destinadas ao usuário devem preservar alterações recebidas no último pacote e explicitar a substituição de dados.

## Documentos

1. [Pesquisa e fontes](docs/01-pesquisa.md) — hipóteses, limitações e protocolo de validação.
2. [Oferta e modelo econômico](docs/02-oferta.md).
3. [Tráfego, eventos e experimentos](docs/03-trafego.md).
4. [Produto e arquitetura online](docs/04-produto-e-arquitetura.md).
5. [Criativos e Vmake](docs/05-criativos-vmake.md).
6. [Plano de 30 dias](docs/06-plano.md).

As fontes externas retornaram bloqueio 403 do proxy em 23/10/2026. Esta entrega contém estratégia fundamentada em hipóteses explícitas e um roteiro de pesquisa aprofundada, **não uma pesquisa externa concluída**. Preços concorrentes, anúncios ativos, resultados e recursos do Vmake não foram verificados.
