-- rls_auto_enable() é chamada pelo event trigger do Supabase; não precisa ser chamável via /rest/v1/rpc.
revoke execute on function public.rls_auto_enable() from public, anon, authenticated;
