# Exemplos de fluxos

Há duas categorias de fluxos no AP2: Human Present e Human Not Present.

  - *Human Present*: o usuário aprova **diretamente** os closed Checkout e
    Payment Mandates.
  - *Human Not Present*: o usuário aprova open Checkout e Payment Mandates,
    enquanto o agente, atuando de forma autônoma, os apresenta junto com closed
    Checkout e Payment Mandates assinados pelo agente.

Um fluxo Human Not Present pode ser convertido em um fluxo Human Present pelo
Merchant (ou pelo Credential Provider) ao retornar um erro
`unresolved_constraint` e trazer o usuário de volta ao processo para aprovar os
closed Mandates.

Todos os fluxos abaixo são exemplos não normativos. Eles pressupõem que o
cadastro adequado e as User Credentials necessárias foram configurados
previamente.

## Human Present

Este é o fluxo `direct`, em que o usuário está presente para aprovar
diretamente os closed Payment e Checkout Mandates.

<figure>
  <img src="../../assets/ap2_hp_flow.svg" style="width:800px" alt="Diagram showing the overall Human Present flow in AP2">
  <figcaption align="center">Fluxo Human Present</figcaption>
</figure>

Este fluxo tem duas fases:

**Fase 1: compra**

<figure>
  <img src="../../assets/ap2_hp_shopping.svg" style="width:800px" alt="Human Present Shopping flow">
  <figcaption align="center">Fluxo de compra Human Present</figcaption>
</figure>

  1. O usuário inicia a compra com o Shopping Agent.
  2. O Shopping Agent se comunica com o Merchant e monta um carrinho.
  3. O Shopping Agent vai para o checkout. O Merchant cria um Checkout assinado
     e exige um mandate adequado para continuar.
  4. O Shopping Agent obtém as Instrument Options existentes no Credential
     Provider e seleciona uma.

**Fase 2: pagamento**

<figure>
  <img src="../../assets/ap2_hp_payment.svg" style="width:800px" alt="Human Present Payment flow">
  <figcaption align="center">Fluxo de pagamento Human Present</figcaption>
</figure>

  1. O Shopping Agent monta o conteúdo do Payment Mandate e do Checkout Mandate e
     solicita a aprovação do usuário por meio de uma Trusted Surface.
     - *Pode ser uma Trusted Surface externa, no modelo de User Credential, ou
       uma interna, no modelo de Trusted Agent Provider.*
  2. A Trusted Surface exibe o conteúdo do Mandate e obtém a autenticação do
     usuário (por exemplo, biometria) e o consentimento.
  3. A Trusted Surface usa a `user_sk` para assinar e criar o Payment Mandate e
     o Checkout Mandate.
     - *O hash do `checkout_jwt` é usado para vincular os Mandates de forma
       permanente.*
     - *No modelo de Trusted Agent Provider, a `user_sk` seria a chave do Agent
       Provider.*
  4. A Trusted Surface devolve os Mandates ao Shopping Agent.
  5. O Shopping Agent envia o Payment Mandate ao Credential Provider, que o
     verifica e cria um token de pagamento.
     - *Como parte desse processo, o Credential Provider pode compartilhar o
       Payment Mandate com a rede de pagamento e receber uma credencial de compra
       com escopo limitado (também chamada de token).*
  6. O Shopping Agent envia esse token e o Checkout Mandate ao Merchant.
  7. O Merchant verifica a integridade e o conteúdo do Checkout Mandate em
     relação ao estado atual do carrinho e, em seguida, inicia o pagamento com o
     token e o hash do `checkout_jwt`.
  8. O Merchant Payment Processor verifica o Payment Mandate incluído no token e
     o vínculo com o hash do `checkout_jwt`.
  9. O Payment Receipt assinado pelo MPP é devolvido ao Shopping Agent, ao
     Credential Provider e à rede, e o Checkout Receipt assinado pelo Merchant é
     devolvido ao Shopping Agent para indicar sucesso.

## Human Not Present

<figure>
  <img src="../../assets/ap2_hnp_flow.svg" style="width:800px" alt="Human Not Present flow">
  <figcaption align="center">Fluxo Human Not Present</figcaption>
</figure>

**Fase 1: compra**

No fluxo Human Not Present, a fase de compra é dividida em duas. Na primeira, o
usuário define uma tarefa de compra para o agente. Na segunda, o agente atua de
forma autônoma para concluir a tarefa sem nova interação humana.

<figure>
  <img src="../../assets/ap2_hnp_shopping.svg" style="width:800px" alt="Human Not Present Shopping flow">
  <figcaption align="center">Fluxo de compra Human Not Present</figcaption>
</figure>

**Fase 1a: compra (Human Present)**

Nesta fase, o usuário concede ao agente autorização para comércio autônomo na
forma de open Checkout e Payment Mandates.

  1. O usuário inicia a compra com o Shopping Agent.
  2. O Shopping Agent monta o conteúdo adequado dos Mandates `open` para a
     sessão de compra e solicita a aprovação do usuário por meio de uma Trusted
     Surface.
     - *Isso define um conjunto de constraints dentro do qual o Shopping Agent
       pode atuar sem precisar de nova autorização do usuário.*
  3. A Trusted Surface exibe o conteúdo do Mandate e obtém a autenticação do
     usuário (por exemplo, biometria) e o consentimento.
  4. A Trusted Surface usa a `user_sk` para assinar e criar o open Checkout
     Mandate e o open Payment Mandate.
     - *O hash do open Checkout Mandate é incluído no open Payment Mandate para
       vinculá-los de forma permanente.*
     - *A `agent_pk` é incluída como claim de confirmação para restringir o uso
       do Mandate ao remetente.*
     - *No modelo de Trusted Agent Provider, a `user_sk` seria a chave do Agent
       Provider.*

O usuário então sai da sessão, depois de delegar a tarefa de compra ao Shopping
Agent.

**Fase 1b: compra (Human Not Present)**

Nesta fase, o agente monta de forma autônoma um Checkout que, segundo sua
avaliação, cumpre a tarefa atribuída.

  1. O Shopping Agent se comunica com o Merchant e monta um carrinho.
  2. O Shopping Agent vai para o checkout. O Merchant cria um Checkout assinado
     e exige um mandate adequado para continuar.

**Fase 2: pagamento (Human Not Present)**

Nesta fase, o agente conclui o checkout usando os Mandates recebidos.

<figure>
  <img src="../../assets/ap2_hnp_payment.svg" style="width:800px" alt="Human Not Present Payment flow">
  <figcaption align="center">Fluxo de pagamento Human Not Present</figcaption>
</figure>

  1. O Shopping Agent seleciona os open Mandates existentes cujas constraints se
     aplicam ao Checkout recebido.
     - *O mecanismo de seleção de Mandates está fora do escopo desta
       especificação.*
     - *Para evitar gasto em duplicidade, o Shopping Agent MUST NOT (não pode)
       criar vários Mandates sobrepostos até receber um Action Receipt indicando
       erro. Veja a seção Implementation Considerations para mais detalhes.*
  2. O Shopping Agent monta o conteúdo do Payment Mandate e do Checkout Mandate e
     assina os dois closed Mandates usando a `agent_sk`.
     - *O hash do `checkout_jwt` é usado para vinculá-los de forma permanente.*
     - *A propriedade `sd_hash` do `kb-sd-jwt` é usada para vincular o closed
     mandate ao open*
  3. O Shopping Agent envia os Payment Mandates (open e closed) ao Credential
     Provider, que os verifica e cria um token de pagamento.
     - *Como parte desse processo, o Credential Provider pode compartilhar o
       Payment Mandate com a rede de pagamento e receber uma credencial de compra
       com escopo limitado (também chamada de token).*
  4. O Shopping Agent envia esse token e os Checkout Mandates (open e closed) ao
     Merchant.
  5. O Merchant verifica a integridade e o conteúdo do closed Checkout Mandate em
     relação ao estado atual do carrinho e verifica se as constraints do open
     Checkout Mandate foram atendidas. Em seguida, inicia o pagamento com o token,
     o hash do `checkout_jwt` e o hash do open Checkout Mandate.
  6. O Merchant Payment Processor verifica os Payment Mandates incluídos no
     token, assim como os vínculos com o hash do `checkout_jwt` e com o hash do
     open Checkout Mandate.
  7. O Payment Receipt assinado pelo MPP é devolvido ao Shopping Agent, ao
     Credential Provider e à rede, e o Checkout Receipt assinado pelo Merchant é
     devolvido ao Shopping Agent para indicar sucesso.
