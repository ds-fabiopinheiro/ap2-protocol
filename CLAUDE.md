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
- Variáveis (production, preview, development; tipo plain):
  - `VITE_AGENT_URL=https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent`
  - `VITE_MERCHANT_TRIGGER_URL=https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/merchant`
  - `VITE_FLOW=card`
- Deployment Protection: "Standard Protection" (padrão). Verificado que a URL
  de produção abre sem login (título da página: "Shopping Agent — AP2
  Human-Not-Present"). As URLs de preview exigem login do Vercel.
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

**Não testado:** conversa real com o agente (falta chave de LLM no Space) e o
sincronismo contra o Supabase real (falta `SUPABASE_SECRET_KEY` no Space).

## 6. Pendências, em ordem

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

### P3 — URL do agent card (código concluído; falta validar no Space)

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

Falta: Factory rebuild do Space e conferir
`https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent/.well-known/agent-card.json`
(esperado: `"url": "https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent"`).

### P4 — Rebuild automático do Space (workflow criado; depende do usuário)

`.github/workflows/hf-space-rebuild.yml`: roda em push no `homolog-deploy`
que altere `code/samples/python/**`, `code/sdk/**`, `deploy/hf-space/**` ou
`pyproject.toml`, e manualmente (`workflow_dispatch`). Instala
`huggingface_hub` e chama
`HfApi(token=HF_TOKEN).restart_space("ds-fabiopinheiro/ap2-homolog-backend", factory_reboot=True)`.
Falha com mensagem explícita se o secret não existir.

Falta (ação do usuário): criar token fine-grained do HF com escrita só no
Space, cadastrar como secret `HF_TOKEN` em GitHub → Settings → Secrets and
variables → Actions, e confirmar que o GitHub Actions está habilitado no fork
(aba Actions). Depois, disparar o workflow manualmente uma vez para validar.

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

### P7 — Rede do ambiente "AP2-Google"

Com "Acesso à rede: Confiável", a sessão original não conseguiu acessar
`ai-gateway.vercel.sh`. Se precisar testar endpoints a partir do Claude Code,
peça ao usuário para liberar `*.hf.space`, `*.supabase.co`, `*.vercel.app` e
`ai-gateway.vercel.sh`.

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
- Depois de mudar código do backend, é preciso "Factory rebuild" no Space.
  Com o secret `HF_TOKEN` cadastrado (P4), o workflow `hf-space-rebuild.yml`
  faz isso no push; sem o secret, o rebuild continua manual.

## 8. Teste local rápido

```bash
uv sync --package ap2-samples
APP_DIR=$PWD TEMP_DB_DIR=/tmp/ap2/temp-db LOGS_DIR=/tmp/ap2/logs \
  GOOGLE_API_KEY=... bash deploy/hf-space/start.sh
curl localhost:7860/a2a/shopping_agent/.well-known/agent-card.json
curl "localhost:7860/merchant/state?item_id=x"
```
(precisa de `nginx` instalado)
