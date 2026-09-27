/**
 * Formats an amount for display in pt-BR, e.g. 450 -> "US$ 450,00".
 * Falls back to "<value> <currency>" when the currency code is not valid.
 */
export function formatMoney(value: number, currency = 'USD'): string {
  try {
    return new Intl.NumberFormat('pt-BR', {style: 'currency', currency})
        .format(value);
  } catch {
    return `${value.toFixed(2).replace('.', ',')} ${currency}`;
  }
}

/** Formats a dollar amount, e.g. 450 -> "US$ 450,00". */
export function formatUsd(value: number): string {
  return formatMoney(value, 'USD');
}

/** Formats an amount given in minor units (cents), e.g. 45000 -> "US$ 450,00". */
export function formatMinorUnits(amount: number, currency = 'USD'): string {
  return formatMoney(amount / 100, currency);
}

/** Formats a date/time in pt-BR. */
export function formatDateTime(
    date: Date, options?: Intl.DateTimeFormatOptions): string {
  return date.toLocaleString('pt-BR', options);
}
