-- Espelho do diretório TEMP_DB_DIR usado pelos papéis do AP2 (chaves, token store, inventário, mandates).
create table if not exists public.ap2_state_files (
  name        text primary key,
  content     text not null,
  sha256      text not null,
  size_bytes  integer not null,
  updated_at  timestamptz not null default now(),
  deleted_at  timestamptz
);
comment on table public.ap2_state_files is 'Mirror of the AP2 sample TEMP_DB_DIR so state survives container restarts on the HF Space.';

-- Trilha de auditoria: cada Mandate SD-JWT emitido (nunca apagado, mesmo após reset do demo).
create table if not exists public.ap2_mandates (
  id             text primary key,
  kind           text not null check (kind in ('checkout', 'payment')),
  stage          text not null check (stage in ('open', 'closed')),
  sdjwt          text not null,
  sha256         text not null,
  first_seen_at  timestamptz not null default now()
);
create index if not exists ap2_mandates_first_seen_idx on public.ap2_mandates (first_seen_at desc);
comment on table public.ap2_mandates is 'Audit trail of every AP2 Checkout/Payment Mandate (open and closed) produced in homologation.';

-- Eventos operacionais (start do container, sync, erros).
create table if not exists public.ap2_events (
  id          bigint generated always as identity primary key,
  source      text not null,
  event       text not null,
  detail      jsonb not null default '{}'::jsonb,
  created_at  timestamptz not null default now()
);
create index if not exists ap2_events_created_idx on public.ap2_events (created_at desc);

-- Acesso somente pelo backend (service_role). RLS ligado e sem políticas = anon/authenticated sem acesso.
alter table public.ap2_state_files enable row level security;
alter table public.ap2_mandates   enable row level security;
alter table public.ap2_events     enable row level security;

revoke all on public.ap2_state_files, public.ap2_mandates, public.ap2_events from anon, authenticated;
grant select, insert, update, delete on public.ap2_state_files, public.ap2_mandates, public.ap2_events to service_role;
grant usage, select on sequence public.ap2_events_id_seq to service_role;
