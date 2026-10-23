# Plano de tráfego e experimentos

Orçamento provisório: R$ 1.500/mês, exclusivamente mídia. Não aprovado para gasto. Criativos, ferramentas, impostos e operação são adicionais. Nenhuma conta ou campanha foi conectada.

## Pré-requisitos de lançamento

Página publicada com HTTPS e canal real de inscrição; identidade da empresa; termos e privacidade; consentimento quando necessário; conta anunciante e faturamento; atendimento; evento testado ponta a ponta; exclusão de dados pessoais dos parâmetros. O protótipo atual não capta leads nem dispara eventos. Não direcionar anúncios para ele ainda.

## Distribuição para aprender

Começar em um canal (hipótese: Meta) para não pulverizar orçamento. R$ 900 na primeira fase: R$ 30/dia por 30 dias, um conjunto de público e até 3 criativos. Reservar R$ 600 para substituir peças ou ampliar o teste após revisar sinais, sem obrigação de gastar a reserva. A duração pode ser reduzida; orçamento é teto. Com esse volume, resultados tendem a ser exploratórios e não sustentam certezas estatísticas.

Público: um nicho, Brasil/região coerente com suporte, 18+, sem presumir dificuldade financeira pessoal do espectador. Validar segmentações disponíveis na conta; não inventar interesses. Testar primeiro ganchos mantendo oferta e página fixas. Só depois variar público ou preço. Google Search é segundo teste se houver demanda de intenção observável e orçamento adicional; TikTok orgânico pode testar linguagem sem mídia paga.

## Matriz de teste

| Rodada | Variável | Comparação | Métrica de decisão |
|---|---|---|---|
| 1 | Gancho | documento perdido × cobrança esquecida × rotina do dia | Lead qualificado e ativação por mensagem |
| 2 | Demonstração | gravação da rotina × apresentador | Taxa de ativação e custo por ativado |
| 3 | Oferta | conversa de piloto × teste guiado | Pagamento e suporte por cliente |

Não declarar vencedor com 1 compra. Registrar impressão, CPM, clique de saída, CPC, sessão, lead válido, qualificado, ativação e pagante; distinguir métricas da plataforma e do produto. Muitos cliques sem lead: investigar mensagem, velocidade e CTA. Leads sem ativação: problema de fit/onboarding. Ativação sem pagamento: oferta/preço/valor. Não resolver toda falha aumentando verba.

## Eventos e atribuição a implementar

`landing_view`, `lead_submitted`, `lead_qualified`, `pilot_started`, `activation_completed`, `subscription_paid`, `subscription_cancelled`. Definir ID não pessoal, data, canal, campanha, criativo, UTM, event_id e coorte. Não enviar nome de cliente, CPF, nota, valor de conta, documento ou texto financeiro para pixels. Deduplicar evento browser/servidor se usar ambos. Pagamento confirmado por webhook validado, nunca por clique em botão. Nenhum evento implementado neste protótipo.

UTMs: `utm_source=meta&utm_medium=paid_social&utm_campaign=piloto_servicos_v1&utm_content=gancho_documento_v1`. Declarar janelas separadas: primeiro contato e conversão; registrar regra usada. Esperar a janela completar antes de comparar coortes. Métricas no painel são entradas manuais, sem atribuição automática.

## Regras operacionais propostas

Revisão após 72h ou R$ 90 por criativo, o que acontecer depois, respeitando teto de gasto. Esses valores são limites de inspeção, não significância. Se rastreamento falhar, parar o teste. Se gastar até o CAC máximo planejado sem pagante e sem pipeline qualificado, pausar e investigar antes de mais verba; venda com ciclo mais longo exige acompanhamento da coorte. Escalar só após pagamentos, ativação, margem e retenção observadas; aumentar em passos pequenos definidos na conta pelo responsável.

Hipóteses virais: checklist de fechamento semanal sem dados financeiros expostos; demonstração “caos → próximo passo”; modelo educativo para cobrar de forma respeitosa; convite voluntário após benefício observado. Medir compartilhamentos, leads e retenção. Não há receita garantida para viralizar, e compartilhamento não substitui venda. Programa de indicação só com antifraude e custo definido, sem acesso a contatos do usuário.
