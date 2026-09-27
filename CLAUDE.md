# CLAUDE.md — Ambiente de homologação do AP2 (branch `homolog-deploy`)

Este arquivo passa o contexto do trabalho feito em 25/09/2026 para as próximas
sessões do Claude Code. Leia inteiro antes de alterar qualquer coisa.

## 1. Objetivo

Publicar o cenário `code/samples/python/scenarios/a2a/human-not-present/cards`
do Agent Payments Protocol (AP2) em um ambiente de homologação público, que
qualquer pessoa possa validar por um link:

- frontend no Vercel;
- backend (os 4 papéis do AP2) em um Hugging Face Space;
- banco de dados no Supabase.

Repositório: `ds-fabiopinheiro/ap2-protocol` (fork de
`google-agentic-commerce/AP2`, sem alterações no `main`).
Todo o trabalho está no branch **`homolog-deploy`**. Não altere o `main`.

## 2. Recursos criados

| Plataforma | Recurso | Identificadores |
|---|---|---|
| GitHub | branch `homolog-deploy` | commits listados na seção 4 e na P5; histórico completo com `git log --oneline main..homolog-deploy` |
| Vercel | projeto `ap2-homolog-frontend` | team `fabiopinheiro-projects` (`team_TFJpulVK8Dcufy5SIecwChUh`), projeto `prj_ndPs9jLlb7NFC3agQqe4DoUEiz1H`, URL https://ap2-homolog-frontend.vercel.app |
| Hugging Face | Space `ds-fabiopinheiro/ap2-homolog-backend` | SDK Docker, hardware CPU Basic (gratuito), público, URL https://ds-fabiopinheiro-ap2-homolog-backend.hf.space |
| Supabase | projeto `ap2-homolog-db` | org `xrusgxpywgadhhgalcfs` (plano Pro), ref `vpermplrecflxtitndgd`, região `us-east-2` (Ohio), compute Micro, URL https://vpermplrecflxtitndgd.supabase.co |

Custo: o projeto Supabase adiciona cerca de US$ 10/mês à organização Pro (o
crédito de compute de US$ 10 já é consumido pelo projeto
`monitor-hashtag-linkedin`). Vercel e HF Space estão em planos sem custo
adicional para este uso.

## 3. Arquitetura

```
Navegador ──> Vercel (code/web-client, Vite + React)
                 │  VITE_AGENT_URL / VITE_MERCHANT_TRIGGER_URL
                 ▼
HF Space (container Docker, porta pública 7860, nginx)
  /a2a/*       -> 127.0.0.1:8080  shopping_agent_v2 (ADK + A2A, usa LLM)
  /merchant/*  -> 127.0.0.1:8081  merchant_agent_mcp/trigger_server.py
  (interno)       127.0.0.1:8082  credentials_provider_mcp/trigger_server.py
  (interno)       127.0.0.1:8083  merchant_payment_processor_mcp/trigger_server.py
  Servidores MCP (server.py) são iniciados via stdio pelo shopping agent.
  sync_supabase.py espelha TEMP_DB_DIR (/tmp/ap2/temp-db) no Supabase.
                 │  REST (PostgREST) com SUPABASE_SECRET_KEY
                 ▼
Supabase: ap2_state_files, ap2_mandates, ap2_events
```

Só o `shopping_agent_v2` chama LLM. O modelo vem de `AGENT_MODEL`:
- sem `/` (ex.: `gemini-3.1-flash-lite-preview`): cliente Gemini nativo, usa `GOOGLE_API_KEY`;
- com prefixo de provedor (ex.: `vercel_ai_gateway/google/gemini-3.1-flash-lite-preview`):
  LiteLLM, usa a chave do provedor (ex.: `VERCEL_AI_GATEWAY_API_KEY`).

## 4. O que foi feito

### 4.1 Código (branch `homolog-deploy`)

| Commit | Conteúdo |
|---|---|
| `5b03f5a` | `deploy/hf-space/`: `Dockerfile`, `start.sh`, `nginx.conf`, `sync_supabase.py`, `SPACE_README.md` |
| `10b3878` | `deploy/README.md`: arquitetura, variáveis de ambiente, limitações |
| `103d8d0` | `code/samples/python/pyproject.toml`: dependência `litellm>=1.76.0` |
| `dba430d` | `shopping_agent_v2/shopping_agent/agent.py`: função `_resolve_model()` (LiteLLM quando `AGENT_MODEL` tem `/`) |
| `7db0f41` | `supabase/migrations/`: as 2 migrations já aplicadas no projeto |
| `e5ed159` | `supabase/config.toml` |
| `8475da2` | `code/web-client/src/utils/mandateEntries.ts`: remove import e variáveis não usadas que faziam `tsc` falhar no `npm run build` (erro do repositório original; o `run.sh` original usa `npm run dev` e não passava por `tsc`) |
| `53b7c9f` (merge do PR #5) | Web client em pt-BR: textos da interface, `lang="pt-BR"`, valores com `Intl.NumberFormat('pt-BR', USD)` (`src/utils/format.ts`); aviso "Mantenha esta aba aberta: o monitoramento e a compra dependem dela."; erro do agente exibido como "O agente retornou um erro." + texto das parts; "Card •••4242" exibido como "Cartão •••4242" (o mandate assinado não muda); `autoFocus` no campo de mensagem |
| `2121005` (merge do PR #6) | Prompts do Shopping Agent com a regra de responder em pt-BR; `common/model_retry.py` (nova tentativa só em 503) usado por `_resolve_model()`; instrução sobre `product_preview_unavailable` em `consent_agent.md` (ver P8.8) |

Os commits foram feitos pela interface web do GitHub, com o usuário
`ds-fabiopinheiro` como autor, porque a sessão original não tinha permissão de
push. O `uv.lock` não foi commitado: o upstream o removeu no commit `e1ea56d`.

Detalhes dos arquivos de deploy:

- `Dockerfile`: `python:3.11-slim` + git, nginx, curl; `uv==0.8.17`; usuário
  UID 1000 (exigência do HF); clona o branch `homolog-deploy` do GitHub;
  `uv sync --package ap2-samples`; `CMD bash deploy/hf-space/start.sh`.
  A linha `ADD https://api.github.com/repos/.../commits/homolog-deploy` invalida
  o cache do Docker a cada commit novo no branch.
- `start.sh`: define `FLOW=card`, `GOOGLE_GENAI_USE_VERTEXAI=false`, os caminhos
  de estado iguais aos do `run.sh` original; roda `sync_supabase.py restore`;
  sobe os 3 trigger servers e o shopping agent; sobe o `sync_supabase.py watch`
  só se o Supabase estiver configurado; espera o agent card responder; sobe o
  nginx na 7860. Se qualquer processo cair, o container sai com código 1 e o HF
  reinicia.
- `nginx.conf`: expõe apenas `/`, `/a2a/` (sem buffer, para SSE) e
  `/merchant/`. As portas 8082 e 8083 não são publicadas de propósito.
- `sync_supabase.py`: só biblioteca padrão. `restore` baixa
  `ap2_state_files` (sem `deleted_at`) para `TEMP_DB_DIR`. `watch` envia
  arquivos novos/alterados a cada `AP2_SYNC_INTERVAL` s (padrão 2), marca
  apagados com `deleted_at` e grava em `ap2_mandates` os arquivos
  `open_chk_*`, `open_pay_*`, `chk_*`, `pay_*` com extensão `.sdjwt`. Envia só o
  header `apikey` (funciona com chave `sb_secret_` e com service_role legada).

### 4.2 Supabase

- Migration `20260925213004_ap2_homolog_initial_schema`: tabelas
  `ap2_state_files` (name PK, content, sha256, size_bytes, updated_at,
  deleted_at), `ap2_mandates` (id PK, kind checkout|payment, stage open|closed,
  sdjwt, sha256, first_seen_at), `ap2_events` (id identity, source, event,
  detail jsonb, created_at). RLS ligado sem políticas; `anon` e
  `authenticated` sem privilégios; `service_role` com SELECT/INSERT/UPDATE/DELETE.
- Migration `20260925213023_revoke_rls_auto_enable_from_api_roles`: revoga
  EXECUTE de `public.rls_auto_enable()` para `public`, `anon`,
  `authenticated` (alerta do Security Advisor).
- Criação do projeto: "Automatically expose new tables" desmarcado,
  "Enable automatic RLS" marcado.
- Integração GitHub: repositório `ds-fabiopinheiro/ap2-protocol`, working
  directory `.`, "Deploy to production" ligado com branch `homolog-deploy`,
  **"Automatic branching" desligado** (branches de preview geram custo fora do
  spend cap). Não religue sem autorização do usuário.
- Advisor de segurança restante: apenas INFO "RLS enabled no policy" nas 3
  tabelas, que é intencional.

### 4.3 Vercel

- Root directory `code/web-client`, framework Vite, Node 24.x.
- Branch de produção: `homolog-deploy` (Settings → Environments → Production).
- Variáveis (production, preview, development; tipo plain, exceto onde indicado):
  - `VITE_AGENT_URL=https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent`
  - `VITE_MERCHANT_TRIGGER_URL=https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/merchant`
  - `VITE_FLOW=card`
  - `VITE_AUTO_POLL_MS=30000` (tipo Config, cadastrada em Production, Preview
    e Development; alterada de `60000` para `30000` em 26/09/2026 com redeploy
    de produção; o bundle de produção contém `"30000"`; padrão no código
    continua `60000`): intervalo
    em ms do "auto-poll fallback" de `src/hooks/useChat.ts`, que envia
    `check_product_now` ao agente (uma chamada ao LLM por envio) enquanto o
    monitoramento está ativo. `0` desliga. Valor inválido usa `60000`. Lida em
    `src/config.ts`. A consulta de 500 ms a `/merchant/state` não depende dela.
    Até esta mudança o intervalo era fixo em 15000 ms.
  - Variáveis `VITE_*` são lidas no build: alterar no Vercel exige novo deploy.
- Deployment Protection: "Standard Protection" (padrão). Verificado que a URL
  de produção abre sem login (título da página: "Shopping Agent — AP2
  human-not-present", desde o PR #5). As URLs de preview exigem login do Vercel.
- Observação: pelo conector MCP do Vercel, `get_project` e `list_deployments`
  retornaram 404/vazio para este projeto; o painel web mostra o projeto
  normalmente. Use o painel ou a CLI se o conector falhar.

### 4.4 Hugging Face Space

- Arquivos no repositório do Space: `Dockerfile` (cópia de
  `deploy/hf-space/Dockerfile`) e `README.md` (cópia de `SPACE_README.md`, com
  `sdk: docker` e `app_port: 7860`).
- Visibilidade: **Protected** (app público pela URL; arquivos do repositório do
  Space retornam 401 para quem não é dono). Private não serve: exigiria login
  no HF para chamar a API, e o frontend no Vercel é acessado por visitantes
  anônimos.
- Variáveis públicas cadastradas: `SUPABASE_URL`, `AGENT_MODEL=gemini-3.1-flash-lite-preview`.
- Estado verificado: build concluído, container rodando, agent card
  respondendo publicamente em `/a2a/shopping_agent/.well-known/agent-card.json`.

### 4.5 Ambiente do Claude Code "AP2-Google"

Variáveis não sensíveis cadastradas pelo usuário (`AGENT_MODEL`,
`AGENT_MODEL_ALT`, `GOOGLE_GENAI_USE_VERTEXAI`, `GIT_REPO`, `GIT_BRANCH`,
`HF_SPACE_ID`, `HF_SPACE_URL`, `VERCEL_TEAM`, `VERCEL_PROJECT`,
`SUPABASE_PROJECT`) e script de configuração que instala `uv`. Nenhum segredo
deve ser colocado nesse formulário: os valores ficam visíveis para quem usa o
ambiente.

## 5. Testes realizados

Executados no container da sessão original (sem Docker, sem chave de LLM):

| Teste | Resultado |
|---|---|
| `uv sync --package ap2-samples` com `litellm` | OK (litellm 1.102.1, google-adk 1.28.0); provedor `vercel_ai_gateway` presente |
| `start.sh` completo + nginx | 4 serviços no ar; agent card, `/merchant/state`, `/merchant/trigger-price-drop` e preflight CORS OK via :7860; `/credentials-provider/` retorna 404 (esperado) |
| 3 servidores MCP via stdio (`initialize`) | OK |
| `sync_supabase.py` contra PostgREST simulado | restore, upload, auditoria em `ap2_mandates` e `deleted_at` OK |
| `npm run build` do web client | OK após a correção do commit `8475da2` |
| Vercel produção | "Ready", abre sem login |
| HF Space | build OK, container "Running", agent card público OK |

Testes de 27/09/2026 (feitos pelo usuário):

| Teste | Resultado |
|---|---|
| Aceitação do PR #5 no preview do Vercel (1ª rodada) | Interface em pt-BR aprovada com ajustes pedidos: aviso de manter a aba aberta, texto do erro do agente, "Cartão" no recibo e Enter com o campo vazio após recarregar. Nessa rodada apareceram os dois erros de P8.8 |
| Reteste do PR #5 (commit `730cc7f`), preview do Vercel, ~04:30 UTC | Aviso da aba OK; após recarregar, o campo recebe foco e o Enter com campo vazio envia a mensagem inicial; bundle com "Cartão " e "O agente retornou um erro."; `Check product now` (3×) e `Check price now` (1×) inalterados. Aprovado para merge |
| Produção após o merge dos PRs #5 e #6, https://ap2-homolog-frontend.vercel.app, 04:39–04:41 UTC | Workflow "HF Space rebuild" com sucesso (04:36:52); Space em RUNNING com restore de 45 arquivos (04:37:56). Enter com campo vazio enviou a mensagem inicial sem clicar no campo; respostas do agente em pt-BR com valores em US$; Trusted Surface e painel com "Mantenha esta aba aberta..."; queda simulada para US$ 450; "Compra concluída", pedido `f3d6fc00-0ab4-43d3-ae77-9ac030e7b914`, US$ 450,00, "Cartão •••4242"; 4 mandates novos em `ap2_mandates` (open checkout, open payment, closed payment, closed checkout); 9 requisições ao agente, todas HTTP 200; nenhum erro 503 ou de ferramenta |
| Testes unitários do PR #6 (`common/model_retry_tests.py`, Gemini simulado) | 7 casos: 503→503→200 conclui na 3ª chamada com esperas de 2–3,5 s e 4–5,5 s; 503 persistente para em 3 chamadas; 429 (com e sem `Retry-After`), 400 e 500 com 1 chamada; retry pela classe `Gemini` do ADK |

## 6. Pendências, em ordem

### Estado dos PRs e issues em 27/09/2026

| PR | Conteúdo | Estado |
|---|---|---|
| #5 | Web client em pt-BR e ajustes do teste de aceitação | Mesclado (`53b7c9f`) |
| #6 | Prompts em pt-BR, nova tentativa em 503 e instrução sobre `product_preview_unavailable` | Mesclado (`2121005`); rebuild do Space OK |
| #7 | Tradução da documentação da raiz e de `docs/` | Aberto, pronto para revisão, CI verde; merge pelo usuário |
| #8 | Tradução dos READMEs de `code/` | Aberto, CI verde; merge pelo usuário |
| #9 | Backlog v3–v6 em `docs/backlog/` | Aberto, CI verde; merge pelo usuário |

Os PRs #7, #8 e #9 alteram a lista `ignorePaths` do `.cspell.json`; a cada
merge, os outros ficam em conflito nesse arquivo. A resolução é manter as
entradas dos dois lados.

Issues da v3 criadas a partir de `docs/backlog/out/issues/` (PR #9): #10–#38,
milestone #1 "v3 — Merchant Agent (homolog-v3)", hierarquia de sub-issues
Épico → Feature → PBI → Task. EP-V3 = #10; features #11–#13; PBIs #14–#18;
tasks #19–#38. Labels aplicadas: `versão:v3` em todas e `tipo:épico` na #10.
Faltam `tipo:feature`, `tipo:pbi`, `tipo:task` e `área:*`, que precisam ser
criadas no GitHub antes (o conector do GitHub não cria labels). v4, v5 e v6
não foram criadas; aguardam confirmação do usuário.

Tradução pt-BR: o que ficou em inglês e o motivo estão nas descrições dos PRs
#5–#8. Valores trocados com o agente (`Check product now`, `Check price now`,
tipos e campos JSON), nomes de ferramentas, rotas, variáveis `VITE_*` e
conteúdo assinado não são traduzidos. Os arquivos traduzidos ficam em
`ignorePaths` do `.cspell.json`, porque o spellcheck do CI só tem o
dicionário em inglês.

### P1 e P2 — CONCLUÍDAS em 26/09/2026 01:36–01:41 UTC

Secrets cadastrados pelo usuário. Teste feito pelo link do Vercel: preview do
produto → assinatura dos open mandates na Trusted Surface → monitoramento →
price drop (`price=199&stock=10`) → compra autônoma concluída (US$ 199,00,
Card •••4242). Supabase: 4 linhas em `ap2_mandates` (open checkout, open
payment, closed payment, closed checkout) e 18 arquivos em `ap2_state_files`.
Após "Restart space": evento `restore` com 18 arquivos e nenhuma chave de
assinatura regravada (as chaves continuaram as mesmas). O texto abaixo fica
como referência para testes futuros.

### P1 — Secrets no HF Space (ação do usuário, não do Claude)

Em https://huggingface.co/spaces/ds-fabiopinheiro/ap2-homolog-backend/settings →
Variables and secrets → **New secret**:

- `GOOGLE_API_KEY`: chave do Google AI Studio;
- `SUPABASE_SECRET_KEY`: Supabase → Project Settings → API Keys → Secret keys (`sb_secret_...`).

Opcional: `VERCEL_AI_GATEWAY_API_KEY`, se `AGENT_MODEL` passar a usar
`vercel_ai_gateway/...`. Nunca peça ao usuário para colar chaves no chat.

### P2 — Validação ponta a ponta

1. Logs do container: não pode haver `WARNING: GOOGLE_API_KEY is not set` nem
   `Supabase not configured`; deve aparecer `restored N file(s)` e `watching`.
2. Abrir https://ap2-homolog-frontend.vercel.app, enviar a mensagem inicial
   (Enter com campo vazio), assinar o mandate na Trusted Surface.
3. Disparar o price drop pelo comando exibido na interface, ou:
   `curl -X POST "https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/merchant/trigger-price-drop?item_id=<id>&price=<preço>&stock=10"`
4. Conferir no Supabase:
   ```sql
   select id, kind, stage, first_seen_at from ap2_mandates order by first_seen_at desc;
   select name, updated_at, deleted_at from ap2_state_files order by updated_at desc;
   select * from ap2_events order by created_at desc limit 20;
   ```
   Esperado: open checkout, open payment, closed checkout e closed payment.
5. Reiniciar o Space e confirmar que as chaves foram restauradas (mesmos
   arquivos `*_signing_key*` em `ap2_state_files`, sem novas chaves geradas).
6. Se o LLM não seguir o fluxo consent → monitoring → purchase, registrar o
   log do `shopping-agent` antes de mudar prompts.

### P3 — URL do agent card (CONCLUÍDA em 26/09/2026)

Após Factory rebuild do Space, o card público
`https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent/.well-known/agent-card.json`
devolve `"url": "https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent"`.
O texto abaixo fica como referência.

`agent.json` do `shopping_agent_v2` tem
`"url": "http://localhost:8080/a2a/shopping_agent"`. O `start.sh`, antes de
subir os serviços, reescreve esse campo (com Python/`json`) para
`$AP2_PUBLIC_BASE_URL/a2a/shopping_agent`. `AP2_PUBLIC_BASE_URL` tem como
padrão `https://$SPACE_HOST` (variável definida pelo HF Spaces no container).
Sem nenhuma das duas, o arquivo não é alterado. A reescrita muda a formatação
do JSON (arrays em várias linhas) só dentro do container; os valores são os
mesmos.

Teste local: com `SPACE_HOST=exemplo.hf.space`, o card em `:7860` retornou
`https://exemplo.hf.space/a2a/shopping_agent`; sem a variável, retornou
`http://localhost:8080/a2a/shopping_agent` e o arquivo não foi alterado.

### P4 — Rebuild automático do Space (CONCLUÍDA em 26/09/2026)

Secret `HF_TOKEN` cadastrado no GitHub (token fine-grained do HF com leitura e
escrita só no Space). O re-run do workflow "HF Space rebuild" terminou em
Success e o Space entrou em Building. Após o rebuild, o evento `restore`
trouxe 20 arquivos do Supabase. O texto abaixo fica como referência.

`.github/workflows/hf-space-rebuild.yml`: roda em push no `homolog-deploy`
que altere `code/samples/python/**`, `code/sdk/**`, `deploy/hf-space/**` ou
`pyproject.toml`, e manualmente (`workflow_dispatch`). Instala
`huggingface_hub` e chama
`HfApi(token=HF_TOKEN).restart_space("ds-fabiopinheiro/ap2-homolog-backend", factory_reboot=True)`.
Falha com mensagem explícita se o secret não existir.

O secret fica em GitHub → Settings → Secrets and variables → Actions. Para
um rebuild manual: aba Actions → "HF Space rebuild" → Run workflow.

### P5 — Proteção contra uso indevido (parcialmente feito)

Feito (commits `9876609` e `c1bd661`): limite de requisições no nginx.
`/a2a/*` 20/min por visitante (rajada 10) e 120/min no total (rajada 30);
`/merchant/*` 5/s por visitante (rajada 20); `OPTIONS` não conta; resposta
429 em JSON com CORS. O visitante é o último IP do `X-Forwarded-For`; nos logs
do Space o HF envia um único IP público do cliente nesse header (verificado).
Teste em produção: 35 requisições simultâneas a `/merchant/state` → 21×200 e
14×429.

Falta: limite de gasto na chave do modelo (ação do usuário) e, se necessário,
restringir CORS/origem ao domínio do Vercel.

### P6 — Sessões do ADK

As sessões de conversa ficam em memória e são perdidas no restart.
`get_fast_api_app` aceita `session_service_uri` (`postgresql://...`). Usar o
Supabase exige a connection string com a senha do banco (secret) e um driver
Postgres. Não implementado.

### Limitação — monitoramento depende da aba aberta

A consulta a `/merchant/state` (500 ms) e o auto-poll (`VITE_AUTO_POLL_MS`)
rodam no navegador (`code/web-client/src/hooks/useChat.ts`). Com a aba do web
client fechada, nada aciona o agente e a compra não acontece. Navegadores podem
reduzir a frequência de timers em abas em segundo plano. Não há plano de
correção definido.

### P7 — Rede do ambiente "AP2-Google"

Com "Acesso à rede: Confiável", a sessão original não conseguiu acessar
`ai-gateway.vercel.sh`. Se precisar testar endpoints a partir do Claude Code,
peça ao usuário para liberar `*.hf.space`, `*.supabase.co`, `*.vercel.app` e
`ai-gateway.vercel.sh`.

### P8 — Limitações observadas nos testes de 26 e 27/09/2026

Pedido usado no teste de 26/09: "tênis Nike 42 preto, CEP 79040-040, monitorar
7 dias, abaixo de R$ 500". Os itens 1–7 não foram corrigidos; são registros
para decidir depois com o usuário. O item 8 foi corrigido no PR #6.

1. **Moeda:** o mandate foi assinado em USD (máximo 50000 centavos), embora o
   texto do agente falasse em R$. O sample fixa `_DEFAULT_CURRENCY = USD`.
2. **Validade:** os mandates saíram com validade de 1 hora em vez de 7 dias.
   `ttl_seconds` não é repassado e o padrão é 3600.
3. **Endereço:** o endereço/CEP informado não entra nos mandates.
4. **Falha na primeira compra:** a primeira tentativa falhou com
   "Payment transaction_id mismatch"; a segunda concluiu a compra de US$ 499.
   Causa provável: duas tentativas simultâneas (auto-poll e nudge do
   `/merchant/state`). Não confirmado em log.
5. **Cota do Gemini:** nível gratuito (15 RPM, 500 RPD); pico registrado
   23/15 RPM, com erros 429 RESOURCE_EXHAUSTED.
6. **Faturamento Google:** bloqueado por retenção OR_CCR_53 na conta Google,
   caso 5-7433000041726, retorno previsto até 03/10/2026.
7. **Teste de consumo (26/09/2026, 16:29–16:37 UTC, `VITE_AUTO_POLL_MS=60000`,
   um usuário):** mesmo pedido; compra concluída na primeira tentativa
   (pedido `694c5a09…`, US$ 450, cartão de teste •••4242, queda de preço
   simulada pelo `/merchant/trigger-price-drop`). AI Studio: pico 7/15 RPM,
   55,4K/250K TPM, 33 RPD no fim do teste. Estimativa de chamadas ao modelo:
   cerca de 9 no pedido + confirmação + aprovação, cerca de 4 por
   `check_product_now` e cerca de 12 na compra. A queda (16:35:23) só foi
   verificada às 16:35:51 (28 s); a aba do demo estava em segundo plano,
   causa não confirmada. Depois do teste o usuário informou que só ele testa
   e que não passa de 500 RPD; por isso o intervalo foi reduzido para
   `30000` (pico estimado cerca de 11 RPM, ainda não medido).
8. **Erros do teste de aceitação do PR #5 (27/09/2026), corrigidos no PR #6:**
   - `503 UNAVAILABLE` do Gemini (modelo sobrecarregado). Correção: `common/model_retry.py` configura `HttpRetryOptions` do
     cliente `google-genai`, passado por `_resolve_model()` como
     `Gemini(model=…, retry_options=…)` aos três agentes. Repete só HTTP 503,
     no máximo 2 novas tentativas (3 chamadas), esperas de cerca de 2 s e 4 s
     mais até 1 s de variação. Repete só a requisição ao modelo, não o turno
     do agente nem as ferramentas. 429, 400 e 500 não são repetidos: o cliente
     ignora `Retry-After`, e repetir 429 gastaria mais da cota gratuita.
     `RetryingLlmAgent` foi descartado porque repete o turno inteiro (inclusive
     ferramentas de checkout e pagamento) em qualquer exceção e sem espera. O
     caminho LiteLLM (`AGENT_MODEL` com `/`) continua sem nova tentativa.
   - `Tool 'product_preview_unavailable' not found`: o modelo chamou como
     função o nome do JSON que deveria escrever no texto. Correção: nova linha
     na seção A de `consent_agent.md`: "`product_preview_unavailable` não é uma
     ferramenta: escreva o JSON no texto da resposta, sem chamar função."
     Schema e exemplos não mudaram.
   - No teste em produção de 27/09 (04:39–04:41 UTC) nenhum dos dois erros
     apareceu. Uma execução não prova que não voltam; se voltarem, registrar o
     log do `shopping-agent`.

## 7. Regras para as próximas sessões

- Trabalhe no branch `homolog-deploy`; o Vercel publica a cada push e o
  Supabase aplica migrations novas em `supabase/migrations`.
- Toda mudança de schema: nova migration em `supabase/migrations/` (nome
  `<timestamp>_<nome>.sql`) e rode o Security Advisor depois.
- Não commitar segredos. Variáveis `VITE_*` vão para o navegador.
- `ap2_state_files` contém as chaves privadas de assinatura do demo. Aceitável
  só para homologação com dados fictícios.
- Não religar "Automatic branching" do Supabase nem trocar o compute sem
  autorização (custo).
- Não commitar `uv.lock`.
- Idioma: mensagens de commit, títulos e descrições de PR em pt-BR, com o
  prefixo Conventional Commits em inglês (exigido pelo workflow
  `conventional-commits.yml`). Ex.: `docs: traduz README para pt-BR`,
  `feat(web-client): interface em pt-BR`.
- O rebuild do Space é automático: o workflow `hf-space-rebuild.yml` faz
  Factory rebuild a cada push no `homolog-deploy` que altere o backend
  (`code/samples/python/**`, `code/sdk/**`, `deploy/hf-space/**`,
  `pyproject.toml`). Mudanças só no web client, na documentação ou no
  Supabase não reconstroem o Space. Confira o resultado na aba Actions.

## 8. Teste local rápido

```bash
uv sync --package ap2-samples
APP_DIR=$PWD TEMP_DB_DIR=/tmp/ap2/temp-db LOGS_DIR=/tmp/ap2/logs \
  GOOGLE_API_KEY=... bash deploy/hf-space/start.sh
curl localhost:7860/a2a/shopping_agent/.well-known/agent-card.json
curl "localhost:7860/merchant/state?item_id=x"
```
(precisa de `nginx` instalado)
