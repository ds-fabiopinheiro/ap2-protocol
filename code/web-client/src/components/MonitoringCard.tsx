import type {MonitoringStatus} from '../types';
import {formatUsd} from '../utils/format';
import './MonitoringCard.scss';

interface Props {
  status: MonitoringStatus;
  onCheckNow?: () => void;
  triggerCurl?: string;
  pollIntervalSeconds?: number;
  itemName?: string;
}

export function MonitoringCard({
  status,
  onCheckNow,
  triggerCurl,
  pollIntervalSeconds,
  itemName,
}: Props) {
  const current = status.current_price ?? status.price_cap;
  const pct =
    current > 0
      ? Math.min(100, Math.round((status.price_cap / current) * 100))
      : 100;
  const available = status.available ?? false;

  return (
    <div className="msg-agent monitoring-card-container">
      <div className="monitoring-card">
        <div className="monitoring-header">
          <div className="status-dot" />
          <span className="title">Painel de monitoramento</span>
        </div>
        <div className="item-name">
          {itemName ?? status.item_id}
          {itemName && <span className="item-id">{status.item_id}</span>}
        </div>

        <div className="status-grid">
          <div className="status-cell">
            <span className="cell-label">Preço</span>
            <span
              className={`cell-value ${status.current_price != null ? 'has-price' : 'no-price'}`}>
              {status.current_price != null
                ? formatUsd(current)
                : '— verificando'}
            </span>
          </div>
          <div className="status-cell">
            <span className="cell-label">Limite</span>
            <span className="cell-value target">
              {formatUsd(status.price_cap)}
            </span>
          </div>
          <div className="status-cell">
            <span className="cell-label">Disponível</span>
            <span
              className={`cell-value ${available ? 'available-yes' : 'available-no'}`}>
              {available ? '✓ Em estoque' : '✗ Ainda não'}
            </span>
          </div>
        </div>

        <div className="progress-track">
          <div className="progress-bar" style={{width: `${pct}%`}} />
        </div>
        <div className="info-text">
          Mantenha esta aba aberta: o monitoramento e a compra dependem dela.
          A compra será feita automaticamente quando o item estiver disponível
          e dentro do orçamento.
        </div>
        {triggerCurl && (
          <div className="curl-box">
            <div className="curl-label">Simular lançamento (preço + estoque):</div>
            <code className="curl-code">{triggerCurl}</code>
          </div>
        )}
        {pollIntervalSeconds && (
          <p className="poll-text">
            Verificação automática a cada {pollIntervalSeconds} s
          </p>
        )}
        {onCheckNow && (
          <button onClick={onCheckNow} className="check-button">
            Verificar agora
          </button>
        )}
      </div>
    </div>
  );
}
