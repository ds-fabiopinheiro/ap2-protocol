import type {MandateEntry, MandateEntryKind} from '../types';
import {MandateCard} from './MandateCard';
import './MandateViewer.scss';

interface Props {
  mandates: MandateEntry[];
}

/**
 * Order in which to present phases in the viewer.
 * Mirrors the AP2 flow: Request → Open Mandates → Checkout JWT →
 * Closed Mandates → Presentations.
 */
const PHASE_ORDER: Array<{
  title: string;
  blurb: string;
  kinds: MandateEntryKind[];
}> = [
  {
    title: 'Mandate Request',
    blurb: 'Proposta exibida ao usuário, montada pelo Shopping Agent.',
    kinds: ['mandate_request'],
  },
  {
    title: 'Open Mandates',
    blurb:
      'SD-JWTs emitidos pelo Credential Provider que autorizam ações futuras.',
    kinds: ['open_checkout_mandate', 'open_payment_mandate'],
  },
  {
    title: 'Checkout JWT',
    blurb: 'Payload de checkout assinado pelo Merchant e vinculado ao carrinho.',
    kinds: ['checkout_jwt'],
  },
  {
    title: 'Closed Mandates',
    blurb: 'Credenciais delegadas assinadas pelo agente que completam a cadeia.',
    kinds: ['closed_checkout_mandate', 'closed_payment_mandate'],
  },
  {
    title: 'Mandate Chains',
    blurb: 'Cadeias SD-JWT completas com os open e closed mandates.',
    kinds: ['mandate_chain'],
  },
  {
    title: 'Presentations',
    blurb: 'Presentations com Key Binding para o Merchant / Credential Provider.',
    kinds: ['presentation'],
  },
];

export function MandateViewer({mandates}: Props) {
  if (mandates.length === 0) {
    return (
      <div className="mandate-viewer-empty">
        <div className="icon">📝</div>
        <div className="title">Nenhum mandate ainda</div>
        <div className="subtitle">
          Os mandates criados nesta sessão de compra aparecem aqui como cartões
          estruturados, com o detalhe completo do SD-JWT.
        </div>
      </div>
    );
  }

  return (
    <div className="mandate-viewer">
      <div className="viewer-header">
        <div className="viewer-title">Mandates</div>
        <div className="viewer-subtitle">
          {mandates.length} mandate{mandates.length === 1 ? '' : 's'} nesta
          sessão · clique em um cartão para ver o conteúdo decodificado
        </div>
      </div>

      {PHASE_ORDER.map((phase) => {
        const entries = mandates.filter((m) => phase.kinds.includes(m.kind));
        if (entries.length === 0) return null;
        return (
          <section key={phase.title} className="phase-section">
            <div className="phase-header">
              <div className="phase-title">{phase.title}</div>
              <div className="phase-blurb">{phase.blurb}</div>
            </div>
            <div className="phase-cards">
              {entries.map((entry) => (
                <MandateCard key={entry.id} entry={entry} />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
