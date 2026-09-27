import type {ProductPreviewUnavailable} from '../types';
import {formatUsd} from '../utils/format';
import './ProductPreviewUnavailableCard.scss';

interface Props {
  preview: ProductPreviewUnavailable;
}

export function ProductPreviewUnavailableCard({preview}: Props) {
  return (
    <div className="msg-agent product-preview-unavailable-container">
      <div className="product-preview-card">
        {/* Badge */}
        <div className="preview-badge">Prévia · ainda não disponível para compra</div>

        {/* Emoji visual */}
        {preview.image_emoji && (
          <div className="emoji-display">{preview.image_emoji}</div>
        )}

        {/* Product info */}
        <div className="product-name">{preview.product_name}</div>
        {preview.product_subtitle && (
          <div className="product-subtitle">{preview.product_subtitle}</div>
        )}

        {/* Metadata grid */}
        <div className="metadata-grid">
          {preview.typical_list_price != null && (
            <div className="meta-item">
              <div className="meta-label">Preço de tabela típico</div>
              <div className="meta-value price">
                {formatUsd(preview.typical_list_price)}
              </div>
            </div>
          )}
          {preview.drop_scheduled_hint && (
            <div className="meta-item">
              <div className="meta-label">Lançamento</div>
              <div className="meta-value drop">
                {preview.drop_scheduled_hint}
              </div>
            </div>
          )}
        </div>

        {/* Status bar */}
        <div className="status-bar">
          <div className="status-dot" />
          <span className="status-text">Aguardando lançamento</span>
        </div>
      </div>
    </div>
  );
}
