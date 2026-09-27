# Considerações de segurança e privacidade

## Considerações de segurança

O comércio agêntico introduz vários riscos de segurança. Dado o estado atual da
segurança de agentes, o AP2 assume que é inviável impedir ataques de prompt
injection. Por isso, todos os LLMs e Agents MUST (obrigatório) ser considerados
potenciais atacantes e estão explicitamente incluídos no modelo de ameaças.

### Checkout manipulado

**Ameaça:**

- Um atacante rouba um Payment Mandate (autorização assinada para o pagamento)
  assinado e autorizado para usá-lo com um Checkout não relacionado.

**Mitigação**

- O Payment Mandate MUST conter uma referência ao Checkout associado.
- Isso é feito via `transaction_id` nos closed Payment Mandates e pela
 constraint `mandate.payment.reference` nos open.

**Ameaça:**

- Um atacante reutiliza um open Payment Mandate com outro closed Payment
  Mandate.
- Um atacante reutiliza um open Payment Mandate para aprovar outro closed
  Checkout Mandate (autorização assinada para um checkout).

**Mitigação**

- Closed Mandates MUST conter a claim `sd_hash` para vinculá-los ao open
  Mandate apresentado.
- Open Mandates MUST conter a chave do Agent (via claim `cnf`) para que
  apenas o agente consiga criar um Closed Mandate com assinatura válida.

**Ameaça:**

- Um atacante combina um closed Mandate com outro open Mandate.

**Mitigação**

- Closed Mandates MUST conter a claim `sd_hash` para vinculá-los ao open
  Mandate apresentado.

**Ameaça:**

- Um atacante usa um closed Checkout Mandate com outra sessão de checkout.

**Mitigação**

- O Merchant MUST verificar se `checkout_hash` corresponde ao hash do
  `checkout_jwt` mais recente.

### Pagamento manipulado

**Ameaça:**

- Um Shopping Agent ou Agent do Credential Provider manipula o Payment em
  trânsito, ou solicita um pagamento sem o Mandate aprovado pelo usuário (ou
  diferente dele). Isso faz o Credential Provider executar um Payment não
  aprovado pela Trusted Surface.

**Mitigação:**

- O Merchant Payment Processor e o Credential Provider MUST verificar a
  assinatura do usuário no Payment Mandate para garantir sua integridade.
- O `checkout_hash` incluído no `transaction_id` vincula de forma segura o
  pagamento ao Checkout Mandate associado.
- A avaliação de constraints garante que os valores e os recebedores do
  pagamento respeitem os limites autorizados.

### Roubo de Payment Credential

**Ameaça:**

- Um atacante rouba a Payment Credential ou o Token do usuário depois de sua
  liberação para fazer um pagamento em um contexto não autorizado.

**Mitigação:**

- A Payment Credential/Token MUST ONLY (somente) ser liberada ao Merchant após
  o recebimento e a verificação de um Payment Mandate final. Isso vincula o
  token à transação específica.

### Descoberta manipulada

**Ameaça:**

- Um prompt injection faz o Shopping Agent selecionar produtos maliciosos ou
  tomar decisões de compra ruins.

**Mitigação:**

- A assinatura do Merchant garante a integridade da oferta.
- Mesmo que o LLM não faça a melhor escolha, a aplicação das constraints na
  verificação do closed Mandate garante que o pior impacto financeiro e lógico
  fique estritamente limitado.

### Gasto duplo

**Ameaça:**

- Um Shopping Agent sob prompt injection, ou malicioso por outro motivo, tenta
  aprovar vários Checkouts válidos usando o mesmo open Mandate.

**Mitigação:**

- A parte não determinística do Shopping Agent MUST evitar assinar vários
  closed Mandates sobrepostos para o mesmo open Mandate sem receber Receipts
  que rejeitem os Mandates liberados antes.
  - Esses Receipts MUST ter a integridade protegida contra o LLM do Shopping
    Agent.
- Credential Provider, Networks ou MPPs MAY (opcional) rejeitar vários
 Mandates sobrepostos ou invalidar payment tokens emitidos antes.

## Considerações de privacidade

### Constraints de open Checkout e Payment Mandates

As constraints de open Checkout e Payment Mandates MAY conter informações que
não se aplicam ao Checkout específico e que revelariam intenção do usuário sem
necessidade. Selective Disclosure MUST ser usada para preservar a privacidade
do usuário.

Para reforçar a privacidade do usuário, a Trusted Surface MAY inserir digests
 falsos (decoy digests), como descrito na RFC9901, Seção 4.2.5.

### Minimização de dados de Checkout e Payment

Para preservar a privacidade do usuário e o princípio de minimização de dados,
a Selective Disclosure permite que o Checkout Mandate e o Payment Mandate sejam
compartilhados com as partes relevantes para proteger o Checkout e o Payment,
respectivamente. O `checkout_hash` liga esses Mandates, permitindo reuni-los em
caso de disputa.

> Observação: as informações contidas nos Mandates, ou os próprios Mandates,
> podem ser compartilhadas com outras partes se existirem acordos ou canais
> adequados, mas isso está fora do escopo do AP2.

### Ataques de rainbow table

Os digests em SD-JWTs (dos Payment e Checkout Mandates e das Constraints) MUST
incluir um salt com entropia suficiente para impedir que o texto original seja
adivinhado. Veja a RFC9901, Seção 9.1, para mais detalhes.

O `checkout_hash` aproveita a entropia já incluída na assinatura do JWT para
impedir que o conteúdo do Checkout seja adivinhado. Se for usado um algoritmo
de assinatura que não inclua essa entropia (por exemplo, um esquema de
assinatura determinística como `Ed25519`), um salt com entropia suficiente MUST
estar presente no Checkout.
