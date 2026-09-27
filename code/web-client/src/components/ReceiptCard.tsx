import type { PurchaseComplete } from '../types';
import {formatDateTime, formatUsd} from '../utils/format';
import './ReceiptCard.scss';

function getAmountCharge(
  closedMandateContent?: Record<string, unknown>,
): number {
  const amountObj = closedMandateContent?.payment_amount as
    | { amount?: number }
    | undefined;
  const amountValue = amountObj?.amount;
  return typeof amountValue === 'number' ? amountValue / 100 : 0;
}

function getPaymentMethod(
  closedMandateContent?: Record<string, unknown>,
): string {
  const instrument = closedMandateContent?.payment_instrument as
    | Record<string, unknown>
    | undefined;
  if (instrument?.description && typeof instrument.description === 'string') {
    // The description comes from the signed mandate; translate only the
    // displayed text ("Card •••4242" -> "Cartão •••4242").
    return instrument.description.startsWith('Card ')
      ? `Cartão ${instrument.description.slice('Card '.length)}`
      : instrument.description;
  }
  if (instrument?.type && typeof instrument.type === 'string')
    return instrument.type;
  return 'Cartão';
}

interface Props {
  purchase: PurchaseComplete;
  itemName?: string;
}

export function ReceiptCard({ purchase, itemName }: Props) {
  const closedMandateContent = purchase.closed_payment_mandate_content as
    | Record<string, unknown>
    | undefined;
  const amount = getAmountCharge(closedMandateContent);
  const paymentMethod = getPaymentMethod(closedMandateContent);
  const displayName = itemName ?? 'Pedido';

  return (
    <div className="msg-agent receipt-card-container">
      <div className="receipt-card">
        <div className="success-header">
          <div className="success-badge">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path
                d="M4 9l3.5 3.5 6.5-7"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeDasharray="24"
                strokeDashoffset="0"
              />
            </svg>
          </div>
          <div className="title-container">
            <div className="title">Compra concluída</div>
            <div className="subtitle">Autônoma · autorizada por mandate</div>
          </div>
        </div>

        <div className="receipt-body">
          <div className="display-name">{displayName}</div>
          <div className="order-id">{purchase.order_id}</div>

          <div className="info-grid">
            <div className="grid-item">
              <div className="item-label">Valor cobrado</div>
              <div className="item-value">{formatUsd(amount)}</div>
            </div>
            <div className="grid-item">
              <div className="item-label">Pagamento</div>
              <div className="item-value payment-method">{paymentMethod}</div>
            </div>
          </div>

          <div className="chain-box">
            <div className="chain-label">Cadeia da transação</div>
            {[
              {
                label: 'Merchant MCP',
                steps: 'check_product → cart → checkout → complete',
              },
              {
                label: 'Credential Provider MCP',
                steps: 'issue_payment_credential (verifica + emite)',
              },
            ].map((s) => (
              <div key={s.label} className="chain-row">
                <span className="row-label">{s.label}</span>
                <span className="row-value">{s.steps}</span>
              </div>
            ))}
          </div>

          <div className="timestamp">
            {formatDateTime(new Date(), {
              month: 'short',
              day: 'numeric',
              year: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              timeZoneName: 'short',
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
