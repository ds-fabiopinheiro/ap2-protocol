-- Tabelas por ambiente (v3, v4, ...). Cada versão do ambiente de homologação
-- roda num Space próprio e grava o seu estado com a coluna environment
-- (variável AP2_ENV do Space). As tabelas ap2_state_files, ap2_mandates e
-- ap2_events da v2 (homolog-deploy, sem AP2_ENV) não mudam.

-- Espelho do TEMP_DB_DIR de cada ambiente (chaves, token store, inventário, mandates).
create table if not exists public.ap2_env_state_files (
  environment  text not null,
  name         text not null,
  content      text not null,
  sha256       text not null,
  size_bytes   integer not null,
  updated_at   timestamptz not null default now(),
  deleted_at   timestamptz,
  primary key (environment, name)
);
comment on table public.ap2_env_state_files is 'Mirror of the AP2 sample TEMP_DB_DIR per homologation environment (AP2_ENV), so state survives container restarts on each HF Space.';

-- Trilha de auditoria por ambiente: cada Mandate SD-JWT emitido (nunca apagado).
create table if not exists public.ap2_env_mandates (
  environment    text not null,
  id             text not null,
  kind           text not null check (kind in ('checkout', 'payment')),
  stage          text not null check (stage in ('open', 'closed')),
  sdjwt          text not null,
  sha256         text not null,
  first_seen_at  timestamptz not null default now(),
  primary key (environment, id)
);
create index if not exists ap2_env_mandates_env_first_seen_idx on public.ap2_env_mandates (environment, first_seen_at desc);
comment on table public.ap2_env_mandates is 'Audit trail of every AP2 Checkout/Payment Mandate (open and closed) produced in each homologation environment (AP2_ENV).';

-- Eventos operacionais por ambiente (start do container, sync, erros).
create table if not exists public.ap2_env_events (
  id           bigint generated always as identity primary key,
  environment  text not null,
  source       text not null,
  event        text not null,
  detail       jsonb not null default '{}'::jsonb,
  created_at   timestamptz not null default now()
);
create index if not exists ap2_env_events_env_created_idx on public.ap2_env_events (environment, created_at desc);

-- Acesso somente pelo backend (service_role). RLS ligado e sem políticas = anon/authenticated sem acesso.
alter table public.ap2_env_state_files enable row level security;
alter table public.ap2_env_mandates    enable row level security;
alter table public.ap2_env_events      enable row level security;

revoke all on public.ap2_env_state_files, public.ap2_env_mandates, public.ap2_env_events from anon, authenticated;
grant select, insert, update, delete on public.ap2_env_state_files, public.ap2_env_mandates, public.ap2_env_events to service_role;
grant usage, select on sequence public.ap2_env_events_id_seq to service_role;
