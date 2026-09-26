# Ambiente de homologação do AP2

Cenário publicado: `code/samples/python/scenarios/a2a/human-not-present/cards`
(Shopping Agent, Merchant, Credentials Provider e Merchant Payment Processor).

| Camada | Plataforma | Recurso | Origem do deploy |
|---|---|---|---|
| Frontend (`code/web-client`) | Vercel | `ap2-homolog-frontend` → https://ap2-homolog-frontend.vercel.app | push no branch `homolog-deploy` |
| Backend (4 papéis + nginx) | Hugging Face Spaces (Docker) | `ds-fabiopinheiro/ap2-homolog-backend` → https://ds-fabiopinheiro-ap2-homolog-backend.hf.space | rebuild do Space (clona `homolog-deploy`) |
| Banco | Supabase | `ap2-homolog-db` (ref `vpermplrecflxtitndgd`, us-east-2) | migrations em `supabase/migrations`, aplicadas pela integração GitHub no push em `homolog-deploy` |

## Variáveis de ambiente

### HF Space (Settings → Variables and secrets)

| Nome | Tipo | Valor |
|---|---|---|
| `GOOGLE_API_KEY` | Secret | chave do Google AI Studio (usada quando `AGENT_MODEL` não tem `/`) |
| `VERCEL_AI_GATEWAY_API_KEY` | Secret | chave do Vercel AI Gateway (usada quando `AGENT_MODEL` começa com `vercel_ai_gateway/`) |
| `SUPABASE_SECRET_KEY` | Secret | Supabase → Project Settings → API Keys → Secret key (`sb_secret_...`) |
| `SUPABASE_URL` | Variable | `https://vpermplrecflxtitndgd.supabase.co` |
| `AGENT_MODEL` | Variable | `gemini-3.1-flash-lite-preview` ou `vercel_ai_gateway/google/gemini-3.1-flash-lite-preview` |

Opcionais (já têm padrão em `hf-space/start.sh`): `FLOW=card`,
`TEMP_DB_DIR=/tmp/ap2/temp-db`, `LOGS_DIR=/tmp/ap2/logs`, `AP2_SYNC_INTERVAL=2`.

### Vercel (Project → Settings → Environment Variables)

| Nome | Valor |
|---|---|
| `VITE_AGENT_URL` | `https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/a2a/shopping_agent` |
| `VITE_MERCHANT_TRIGGER_URL` | `https://ds-fabiopinheiro-ap2-homolog-backend.hf.space/merchant` |
| `VITE_FLOW` | `card` |

As variáveis `VITE_*` entram no bundle do navegador: não coloque segredos nelas.

## Persistência no Supabase

O sample original guarda estado em arquivos (`TEMP_DB_DIR`). No HF Space esse
disco é apagado a cada restart, então `hf-space/sync_supabase.py`:

1. `restore`: antes dos serviços subirem, baixa `ap2_state_files` para
   `TEMP_DB_DIR` (mantém as mesmas chaves de assinatura entre restarts);
2. `watch`: a cada 2 s envia arquivos novos/alterados, marca os apagados
   (`deleted_at`) e registra cada Mandate em `ap2_mandates`.

Tabelas (schema `public`, RLS ligado, acesso só com a secret key):

| Tabela | Conteúdo |
|---|---|
| `ap2_state_files` | espelho de `TEMP_DB_DIR`, inclusive as chaves privadas de assinatura do demo |
| `ap2_mandates` | trilha de auditoria: cada Checkout/Payment Mandate (open e closed) em SD-JWT; não é apagada no reset do demo |
| `ap2_events` | eventos do container (restore, início do sync) |

Limitações conhecidas:
- As chaves privadas do demo ficam em `ap2_state_files`. Aceitável para
  homologação com dados fictícios; não usar este desenho com chaves reais.
- Sessões do ADK (histórico de conversa) continuam em memória e são perdidas
  no restart do Space.
- O Space não reconstrói sozinho quando o GitHub muda: é preciso
  *Settings → Factory rebuild* no HF (ou um push no repositório do Space).
- Os endpoints `/merchant/*` e `/a2a/*` são públicos (o demo não tem login).
  Qualquer pessoa com o link pode disparar o "price drop" e consumir o LLM.
  O nginx limita as requisições (resposta 429 em JSON):
  - `/a2a/*`: 20/min por visitante (rajada de 10) e 120/min no total (rajada de 30);
  - `/merchant/*`: 5/s por visitante (rajada de 20);
  - preflight CORS (`OPTIONS`) não conta.
  O visitante é identificado pelo último IP do `X-Forwarded-For` (adicionado
  pelo proxy do HF). Mantenha também um limite de gasto na chave do modelo.

## Teste local do container sem Docker

```bash
uv sync --package ap2-samples
APP_DIR=$PWD TEMP_DB_DIR=/tmp/ap2/temp-db LOGS_DIR=/tmp/ap2/logs \
  GOOGLE_API_KEY=... bash deploy/hf-space/start.sh
curl localhost:7860/a2a/shopping_agent/.well-known/agent-card.json
```
