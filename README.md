# Caixa Leve — projeto de produto financeiro

Estrutura inicial para validar um SaaS brasileiro de organização financeira para prestadores de serviço. Nome provisório, sem pesquisa de marca. A aplicação implementada é um **painel local de gestão do projeto**, com protótipo da página de venda. OCR, documentos, pagamentos, notificações, anúncio e integração com IA ainda não foram implementados.

## Executar

Requer Python 3.12+, sem pacotes externos:

```sh
cd /workspace/SAAS-FINANCE
python server.py
```

No computador em que o servidor estiver rodando, abra a porta 8000 no navegador; `/` é o painel e `/landing` é a página de oferta. No ambiente de nuvem, uma publicação com acesso pelo seu navegador ainda depende de hospedagem e autenticação. Não há link público disponível. O servidor escuta somente loopback por padrão; não o exponha diretamente à internet.

```sh
python -m unittest discover -s tests -v
node --check web/app.js
```

## O que está pronto

- Edição de oferta, orçamento, tarefas, decisões, roteiros e resultados manuais de campanhas.
- CPL, conversão e CAC de mídia calculados a partir dos dados informados; sem números de performance inventados.
- Persistência atômica, controle de revisão para evitar sobrescritas entre sessões, exportação/importação JSON.
- Landing page honesta sobre o estágio do produto, sem checkout nem captação de leads fictícios.

## Compartilhar o contexto com o assistente

O estado inicial está em `data/seed.json`. Ao salvar no navegador, o estado ativo passa a `data/state.json`, ignorado pelo Git para não publicar informações comerciais ou pessoais. Neste mesmo workspace, o assistente pode consultar o arquivo e atualizar pela API `GET/PUT /api/state`, incluindo a revisão atual. Recarregue o painel após atualizações pelo chat. Não há chamada automática a modelos nem integração garantida entre sessões. Em outro ambiente, importe uma exportação ou restaure seu backup; Git sozinho não sincroniza o estado privado.

Para uso online com contas e acesso por vários dispositivos, seguir `docs/04-produto-e-arquitetura.md`. Não colocar documentos financeiros, CPFs, dados bancários ou credenciais neste painel local.

## Documentos

1. [Pesquisa e fontes](docs/01-pesquisa.md) — hipóteses, limitações e protocolo de validação.
2. [Oferta e modelo econômico](docs/02-oferta.md).
3. [Tráfego, eventos e experimentos](docs/03-trafego.md).
4. [Produto e arquitetura online](docs/04-produto-e-arquitetura.md).
5. [Criativos e Vmake](docs/05-criativos-vmake.md).
6. [Plano de 30 dias](docs/06-plano.md).

As fontes externas retornaram bloqueio 403 do proxy em 23/10/2026. Esta entrega contém estratégia fundamentada em hipóteses explícitas e um roteiro de pesquisa aprofundada, **não uma pesquisa externa concluída**. Preços concorrentes, anúncios ativos, resultados e recursos do Vmake não foram verificados.
