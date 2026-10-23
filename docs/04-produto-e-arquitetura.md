# Produto, painel e caminho para operação online

## O que este commit entrega

Painel de projeto servido por Python, estado JSON local, API de leitura/escrita e landing estática. Sem contas de usuários, OCR, upload de notas, lembretes reais, WhatsApp, cobrança, Pix ou chamada ao modelo. As tarefas comerciais e os criativos são reais como planejamento; as funcionalidades do SaaS são backlog. Não confundir painel de planejamento com produto financeiro.

## MVP financeiro em ordem

1. Identidade, empresas separadas, autorização por objeto e trilha de auditoria.
2. Upload privado com limites de tipo/tamanho, varredura, URLs temporárias e política de retenção; nunca bucket público. Validar por conteúdo, não só extensão.
3. Extração de data, valor, fornecedor e categoria, com confiança por campo, fila de erro e revisão humana. Duplicatas por hash e critérios de negócio. Não marcar documento como liquidado sem confirmação apropriada.
4. Contas a pagar/receber, vencimentos, status e responsável. Fuso por empresa. Recorrência com idempotência e tratamento de alteração de data.
5. Lembrete in-app/e-mail; WhatsApp somente depois de validar política, templates e opt-in do provedor. Filas, retries, deduplicação e recibos. Pagamento confirmado cancela lembrete pendente.
6. Resumo semanal e exportação para contador. Medir tempo de revisão e correções antes de automatizar.

## Hospedagem e conexão com o assistente

Para acesso permanente no navegador: frontend e API em host com HTTPS, PostgreSQL, migrações, backups com restauração testada, autenticação e sessões seguras; separar tenants e papéis. Storage privado e fila de tarefas. Escolher fornecedor depois de região, custo e tratamento de dados. Este servidor local não é essa implementação e não deve ser publicado sem autenticação.

O painel pode guardar projetos, experimentos, campanhas, criativos e decisões com IDs e histórico. A conexão com o assistente deve ocorrer via backend autenticado, com chave apenas no servidor, contexto limitado e ações validadas. Guardar sugestões antes de aplicar; exigir confirmação para gasto/lançamento/comunicação. Este chat não fornece uma API automática de memória. É necessário integrar um provedor de modelo ou ferramenta autenticada; isso terá custos e credenciais a configurar.

No workspace atual, ler `/api/state` ou data/state.json já permite colaboração manual pelo chat. Para outro dispositivo/sessão: exportar/importar JSON ou usar futuramente o banco hospedado. Não há sincronização automática Git ↔ dados privados. Publicar código não publica serviço nem cria URL de navegador.

## Modelo de dados futuro

Tenant, Membership, Document, Extraction, LedgerEntry, Reminder, DeliveryAttempt, AuditEvent, Subscription. Todas as entidades de negócio com tenant_id e políticas testadas; valores monetários em centavos/decimal, não float. Campos de documento extraído separados do lançamento confirmado. Lembrete não executa pagamento. Identificador de cobrança/Pix somente via provedor autorizado se essa fase for aprovada.

## Portões antes de dados reais

Termos, finalidade e base legal definidas; retenção e exclusão, exportação, contrato com operadores, controle de acesso, criptografia em trânsito/repouso, logs sem conteúdo financeiro, procedimento de incidente. Consultar orientação oficial e assessoria conforme escopo. Testar isolamento entre empresas, expiração de links, retry duplicado, revisão errada de valor e exclusão. Tokens e documentos não vão para Git, pixel ou prompt por padrão.
