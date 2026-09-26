#!/usr/bin/env python3
"""Espelha o TEMP_DB_DIR dos samples do AP2 no Supabase.

Os papéis do AP2 (Shopping Agent, Merchant, Credentials Provider e Merchant
Payment Processor) compartilham estado por arquivos em TEMP_DB_DIR: chaves de
assinatura, token store, inventário e os Mandates SD-JWT. No HF Space o disco
do container é apagado a cada restart, então este script:

  restore  Baixa os arquivos salvos no Supabase para TEMP_DB_DIR. Roda uma vez,
           antes dos serviços subirem, para que as chaves continuem as mesmas.
  watch    Fica rodando em paralelo aos serviços. A cada AP2_SYNC_INTERVAL
           segundos envia arquivos novos ou alterados, marca os apagados e
           registra cada Mandate novo em ap2_mandates (trilha de auditoria).

Usa só a biblioteca padrão e a REST API do Supabase (PostgREST).

Variáveis de ambiente:
  SUPABASE_URL            ex.: https://<ref>.supabase.co
  SUPABASE_SECRET_KEY     chave secreta (sb_secret_...) ou a service_role
                          legada; também aceita SUPABASE_SERVICE_ROLE_KEY.
  TEMP_DB_DIR             diretório espelhado.
  AP2_SYNC_INTERVAL       intervalo do watch em segundos (padrão 2).

Sem SUPABASE_URL ou chave, o script avisa e sai com código 0: o backend
continua funcionando, apenas sem persistência.
"""

import hashlib
import json
import logging
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from datetime import datetime, timezone
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [supabase-sync] %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("supabase-sync")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY", ""
)
TEMP_DB = Path(os.environ.get("TEMP_DB_DIR", ".temp-db"))
INTERVAL = float(os.environ.get("AP2_SYNC_INTERVAL", "2"))

# Prefixos usados pelo shopping_agent_v2 ao gravar mandates (mandate_tools.py).
_MANDATE_PREFIXES = (
    ("open_chk_", "checkout", "open"),
    ("open_pay_", "payment", "open"),
    ("chk_", "checkout", "closed"),
    ("pay_", "payment", "closed"),
)
# Arquivos maiores que isso não são espelhados (proteção contra lixo).
_MAX_FILE_BYTES = 2 * 1024 * 1024


class SupabaseError(RuntimeError):
  pass


def _request(method: str, path: str, body=None, prefer: str | None = None):
  url = f"{SUPABASE_URL}/rest/v1/{path}"
  headers = {
      # Só o header apikey: o gateway do Supabase gera o Authorization
      # correspondente tanto para chaves sb_secret_ quanto para JWT legado.
      "apikey": SUPABASE_KEY,
      "Content-Type": "application/json",
      "Accept": "application/json",
  }
  if prefer:
    headers["Prefer"] = prefer
  data = json.dumps(body).encode() if body is not None else None
  req = urllib.request.Request(url, data=data, headers=headers, method=method)
  try:
    with urllib.request.urlopen(req, timeout=20) as resp:
      raw = resp.read()
      return json.loads(raw) if raw else None
  except urllib.error.HTTPError as e:
    detail = e.read().decode(errors="replace")[:500]
    raise SupabaseError(f"{method} {path} -> HTTP {e.code}: {detail}") from e
  except urllib.error.URLError as e:
    raise SupabaseError(f"{method} {path} -> {e.reason}") from e


def _now() -> str:
  return datetime.now(timezone.utc).isoformat()


def _sha256(content: str) -> str:
  return hashlib.sha256(content.encode()).hexdigest()


def _event(event: str, **detail) -> None:
  try:
    _request(
        "POST",
        "ap2_events",
        {"source": "hf-space", "event": event, "detail": detail},
        prefer="return=minimal",
    )
  except SupabaseError as e:
    log.warning("could not record event %s: %s", event, e)


def _scan() -> dict[str, str]:
  """Retorna {nome_relativo: conteúdo} dos arquivos de texto em TEMP_DB."""
  files: dict[str, str] = {}
  if not TEMP_DB.exists():
    return files
  for path in TEMP_DB.rglob("*"):
    if not path.is_file():
      continue
    try:
      if path.stat().st_size > _MAX_FILE_BYTES:
        continue
      files[path.relative_to(TEMP_DB).as_posix()] = path.read_text(
          encoding="utf-8"
      )
    except (UnicodeDecodeError, OSError):
      # Arquivo binário ou em escrita neste instante: tenta de novo no próximo
      # ciclo.
      continue
  return files


def _mandate_row(name: str, content: str) -> dict | None:
  if not name.endswith(".sdjwt") or "/" in name:
    return None
  mandate_id = name[: -len(".sdjwt")]
  for prefix, kind, stage in _MANDATE_PREFIXES:
    if mandate_id.startswith(prefix):
      return {
          "id": mandate_id,
          "kind": kind,
          "stage": stage,
          "sdjwt": content.strip(),
          "sha256": _sha256(content),
      }
  return None


def restore() -> int:
  TEMP_DB.mkdir(parents=True, exist_ok=True)
  rows = _request(
      "GET",
      "ap2_state_files?select=name,content&deleted_at=is.null",
  ) or []
  for row in rows:
    target = (TEMP_DB / row["name"]).resolve()
    if TEMP_DB.resolve() not in target.parents:
      log.warning("skipping unsafe path from database: %s", row["name"])
      continue
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(row["content"], encoding="utf-8")
  log.info("restored %d file(s) into %s", len(rows), TEMP_DB)
  _event("restore", files=len(rows))
  return len(rows)


def watch() -> None:
  known: dict[str, str] = {}  # nome -> sha256 já enviado
  try:
    rows = _request(
        "GET", "ap2_state_files?select=name,sha256&deleted_at=is.null"
    ) or []
    known = {r["name"]: r["sha256"] for r in rows}
  except SupabaseError as e:
    log.warning("could not load remote state, will upload everything: %s", e)

  _event("watch_started", interval_seconds=INTERVAL)
  log.info("watching %s every %ss", TEMP_DB, INTERVAL)

  while True:
    try:
      current = _scan()
      changed = []
      for name, content in current.items():
        digest = _sha256(content)
        if known.get(name) != digest:
          changed.append({
              "name": name,
              "content": content,
              "sha256": digest,
              "size_bytes": len(content.encode()),
              "updated_at": _now(),
              "deleted_at": None,
          })

      if changed:
        _request(
            "POST",
            "ap2_state_files?on_conflict=name",
            changed,
            prefer="resolution=merge-duplicates,return=minimal",
        )
        mandates = [
            m for m in (_mandate_row(r["name"], r["content"]) for r in changed)
            if m
        ]
        if mandates:
          _request(
              "POST",
              "ap2_mandates?on_conflict=id",
              mandates,
              prefer="resolution=ignore-duplicates,return=minimal",
          )
          log.info(
              "audit: %s",
              ", ".join(f"{m['id']} ({m['kind']}/{m['stage']})" for m in mandates),
          )
        for r in changed:
          known[r["name"]] = r["sha256"]
        log.info("synced %d file(s)", len(changed))

      removed = [n for n in known if n not in current]
      for name in removed:
        _request(
            "PATCH",
            f"ap2_state_files?name=eq.{urllib.parse.quote(name, safe='')}",
            {"deleted_at": _now()},
            prefer="return=minimal",
        )
        known.pop(name, None)
      if removed:
        log.info("marked %d file(s) as deleted", len(removed))

    except SupabaseError as e:
      # Falha de rede ou do Supabase não derruba o backend; tenta de novo.
      log.error("%s", e)
    time.sleep(INTERVAL)


def main() -> int:
  if len(sys.argv) != 2 or sys.argv[1] not in ("restore", "watch"):
    print("usage: sync_supabase.py restore|watch", file=sys.stderr)
    return 2
  if not SUPABASE_URL or not SUPABASE_KEY:
    log.warning(
        "SUPABASE_URL or SUPABASE_SECRET_KEY not set: running without"
        " persistence"
    )
    return 0
  if sys.argv[1] == "restore":
    try:
      restore()
    except SupabaseError as e:
      log.error("restore failed, starting with empty state: %s", e)
    return 0
  watch()
  return 0


if __name__ == "__main__":
  sys.exit(main())
