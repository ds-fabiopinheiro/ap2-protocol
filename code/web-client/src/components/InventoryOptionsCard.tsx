import {useState} from 'react';
import type {InventoryMatch, InventoryOptionsArtifact} from '../types';
import {formatUsd} from '../utils/format';
import './InventoryOptionsCard.scss';

interface Props {
  inventory: InventoryOptionsArtifact;
  onSelect?: (itemId: string) => void;
}

function ItemRow({
  item,
  selected,
  onClick,
}: {
  item: InventoryMatch;
  selected: boolean;
  onClick?: () => void;
}) {
  return (
    <div
      className={`item-card ${onClick ? 'clickable' : ''} ${selected ? 'selected' : ''}`}
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onClick?.()}>
      <div className="row-content">
        {selected && (
          <div className="selected-icon">
            <svg width="8" height="8" viewBox="0 0 8 8">
              <path
                d="M1.5 4l2 2 3-3"
                stroke="white"
                strokeWidth="1.5"
                fill="none"
                strokeLinecap="round"
              />
            </svg>
          </div>
        )}
        {!selected && <div className="unselected-circle" />}
        <div className="item-details">
          <div className="item-name">{item.name}</div>
          <div className="item-id">{item.item_id}</div>
        </div>
      </div>
      <div className="price-wrapper">
        <div className="item-price">{formatUsd(item.price)}</div>
        {item.stock != null && (
          <div className="item-stock">{item.stock} em estoque</div>
        )}
      </div>
    </div>
  );
}

export function InventoryOptionsCard({inventory, onSelect}: Props) {
  const [userSelected, setUserSelected] = useState<string | undefined>(
    inventory.selected,
  );
  const [hasConfirmed, setHasConfirmed] = useState(false);
  const selected = userSelected ?? inventory.selected ?? '';
  const canConfirm = !!onSelect && !!selected && !hasConfirmed;

  return (
    <div className="msg-agent inventory-options-container">
      <div className="header-wrapper">
        <div className="icon-wrapper">
          <svg width="10" height="10" viewBox="0 0 10 10">
            <path
              d="M2 5l2 2 4-4"
              stroke="#34d399"
              strokeWidth="1.5"
              fill="none"
              strokeLinecap="round"
            />
          </svg>
        </div>
        <span className="tool-label">Merchant MCP · search_inventory</span>
      </div>
      <div className="item-list">
        {inventory.matches.map((item) => (
          <ItemRow
            key={item.item_id}
            item={item}
            selected={item.item_id === selected}
            onClick={onSelect ? () => setUserSelected(item.item_id) : undefined}
          />
        ))}
      </div>
      <p className="info-text">
        Consultei o estoque do Merchant via Merchant MCP e encontrei{' '}
        {inventory.matches.length}{' '}
        {inventory.matches.length === 1 ? 'opção' : 'opções'}, listadas acima.
        Escolha o item. Em seguida, crio o mandate de compra e começo a
        monitorar o preço.
      </p>
      <div className="status-text">
        {onSelect ? (
          selected ? (
            <>
              Selecionado: <span className="selected-item-id">{selected}</span>
              {hasConfirmed
                ? '. Criando o mandate…'
                : '. Clique em "Confirmar seleção" para criar o mandate.'}
            </>
          ) : (
            'Escolha uma das opções acima.'
          )
        ) : (
          <>
            Selecionado:{' '}
            <span className="selected-item-id">{selected || '—'}</span>
          </>
        )}
      </div>
      {canConfirm && (
        <button
          onClick={() => {
            setHasConfirmed(true);
            onSelect?.(selected);
          }}
          className="confirm-button">
          Confirmar seleção
        </button>
      )}
    </div>
  );
}
