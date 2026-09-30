#!/bin/bash
# Sobe o backend do AP2 (cenário human-not-present / cards) dentro do HF Space.
# Equivalente ao code/samples/python/scenarios/a2a/human-not-present/cards/run.sh,
# sem o web client (que roda no Vercel) e com nginx na porta 7860.
set -euo pipefail

APP_DIR="${APP_DIR:-/app}"
ROLES_DIR="$APP_DIR/code/samples/python/src/roles"
DEPLOY_DIR="$APP_DIR/deploy/hf-space"
PY="$APP_DIR/.venv/bin/python"

export FLOW="${FLOW:-card}"
export GOOGLE_GENAI_USE_VERTEXAI="${GOOGLE_GENAI_USE_VERTEXAI:-false}"
export AGENT_MODEL="${AGENT_MODEL:-gemini-3.1-flash-lite-preview}"

# Estado compartilhado entre os papéis (espelhado no Supabase por sync_supabase.py).
export TEMP_DB_DIR="${TEMP_DB_DIR:-/tmp/ap2/temp-db}"
export LOGS_DIR="${LOGS_DIR:-/tmp/ap2/logs}"
export MERCHANT_TRIGGER_STATE_PATH="$TEMP_DB_DIR/merchant_trigger_state.json"
export AP2_TOKEN_STORE_PATH="$TEMP_DB_DIR/ap2_token_store.json"
export MERCHANT_INVENTORY_PATH="$TEMP_DB_DIR/merchant_inventory.json"
export AGENT_PUBLIC_KEY_PATH="$TEMP_DB_DIR/agent_signing_key.pub"
export MERCHANT_SIGNING_KEY_PATH="$TEMP_DB_DIR/merchant_signing_key.pem"
mkdir -p "$TEMP_DB_DIR" "$LOGS_DIR"

# AP2_ENV separa o estado desta versão no Supabase (vazio na v2); AP2_REF é o
# branch clonado pelo Dockerfile.
echo "[start] FLOW=$FLOW AGENT_MODEL=$AGENT_MODEL TEMP_DB_DIR=$TEMP_DB_DIR AP2_ENV=${AP2_ENV:-} AP2_REF=${AP2_REF:-}"
if [ -z "${GOOGLE_API_KEY:-}" ] && [[ "$AGENT_MODEL" != */* ]]; then
  echo "[start] WARNING: GOOGLE_API_KEY is not set and AGENT_MODEL uses Gemini directly."
fi

# 1) Restaura chaves e estado salvos no Supabase antes de qualquer serviço subir.
"$PY" "$DEPLOY_DIR/sync_supabase.py" restore

# 1b) URL pública no agent card. O HF Spaces define SPACE_HOST no container;
#     sem AP2_PUBLIC_BASE_URL nem SPACE_HOST o agent.json fica como está (localhost).
if [ -n "${SPACE_HOST:-}" ]; then
  export AP2_PUBLIC_BASE_URL="${AP2_PUBLIC_BASE_URL:-https://$SPACE_HOST}"
fi
if [ -n "${AP2_PUBLIC_BASE_URL:-}" ]; then
  "$PY" - "$ROLES_DIR/shopping_agent_v2/shopping_agent/agent.json" "${AP2_PUBLIC_BASE_URL%/}/a2a/shopping_agent" <<'EOF'
import json, sys
path, url = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as f:
  card = json.load(f)
card["url"] = url
with open(path, "w", encoding="utf-8") as f:
  json.dump(card, f, indent=2, ensure_ascii=False)
  f.write("\n")
EOF
  echo "[start] agent card url set to ${AP2_PUBLIC_BASE_URL%/}/a2a/shopping_agent"
fi

pids=()
shutdown() {
  echo "[start] stopping services..."
  kill -TERM "${pids[@]}" 2>/dev/null || true
  wait 2>/dev/null || true
}
trap shutdown EXIT INT TERM

start_service() {
  local name="$1" dir="$2"; shift 2
  echo "[start] starting $name"
  (cd "$dir" && exec "$@") > >(sed -u "s/^/[$name] /") 2>&1 &
  pids+=("$!")
}

# 2) Papéis do AP2 (mesma ordem do run.sh). Os servidores MCP (server.py) não
#    rodam aqui: o Shopping Agent os inicia via stdio quando precisa.
start_service merchant-trigger "$ROLES_DIR/merchant_agent_mcp" "$PY" trigger_server.py
start_service credentials-provider "$ROLES_DIR/credentials_provider_mcp" "$PY" trigger_server.py
start_service payment-processor "$ROLES_DIR/merchant_payment_processor_mcp" "$PY" trigger_server.py
start_service shopping-agent "$ROLES_DIR/shopping_agent_v2" "$PY" run_server.py

# 3) Espelhamento contínuo do TEMP_DB_DIR para o Supabase (só se configurado).
if [ -n "${SUPABASE_URL:-}" ] && [ -n "${SUPABASE_SECRET_KEY:-${SUPABASE_SERVICE_ROLE_KEY:-}}" ]; then
  start_service supabase-sync "$DEPLOY_DIR" "$PY" sync_supabase.py watch
else
  echo "[start] WARNING: Supabase not configured, state will be lost on restart."
fi

# 4) Aguarda o agente responder antes de abrir a porta pública.
for i in $(seq 1 120); do
  if curl -fs -o /dev/null "http://127.0.0.1:8080/a2a/shopping_agent/.well-known/agent-card.json"; then
    echo "[start] shopping agent is up after ${i}s"
    break
  fi
  sleep 1
done

# 5) Proxy público na porta 7860 (a porta exposta pelo HF Space).
echo "[start] starting nginx on :7860"
nginx -e stderr -c "$DEPLOY_DIR/nginx.conf" -g "daemon off;" &
pids+=("$!")

# Se qualquer processo cair, o container termina e o HF Space reinicia.
wait -n "${pids[@]}"
echo "[start] a service exited; shutting down so the Space restarts"
exit 1
