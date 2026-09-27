// Use same origin in dev so Vite proxy forwards /a2a to agent server (localhost:8080)
export const AGENT_URL =
  (import.meta as { env?: { VITE_AGENT_URL?: string } }).env?.VITE_AGENT_URL ??
  "/a2a/shopping_agent";

// Merchant trigger for simulating price drop (curl-able)
export const MERCHANT_TRIGGER_URL =
  (import.meta as { env?: { VITE_MERCHANT_TRIGGER_URL?: string } }).env
    ?.VITE_MERCHANT_TRIGGER_URL ?? "http://localhost:8081";

/** Sent when the user presses Enter with an empty input (demo starter). */
export const DEFAULT_CHAT_STARTER_MESSAGE =
    'Quero comprar um tênis Nike preto com logo branca, tamanho 42. Monitore o preço e compre se ficar abaixo de US$ 500.';

/**
 * Interval (ms) of the auto-poll fallback that asks the agent to re-check the
 * product while monitoring. 0 disables it; missing or invalid values use 60000.
 */
const rawAutoPollMs = (import.meta as { env?: { VITE_AUTO_POLL_MS?: string } })
  .env?.VITE_AUTO_POLL_MS;
const parsedAutoPollMs = Number(rawAutoPollMs);
export const AUTO_POLL_MS =
  rawAutoPollMs !== undefined && rawAutoPollMs.trim() !== "" &&
  Number.isFinite(parsedAutoPollMs) && parsedAutoPollMs >= 0
    ? parsedAutoPollMs
    : 60000;
