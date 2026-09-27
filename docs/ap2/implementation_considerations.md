# Considerações de implementação

## Papéis

A seguir, o que cada papel precisa tratar e exemplos de como esse papel pode ser
implementado no ecossistema de pagamentos.

### Merchant

O Merchant precisa implementar:

  - Endpoints de Catalog e Checkout para o Shopping Agent, permitindo que ele
    execute um commerce protocol, por exemplo como descrito no
    [Universal Commerce Protocol](https://ucp.dev/).
  - Geração de um Checkout JWT assinado.
  - Verificação do [Checkout Mandate](checkout_mandate.md) (autorização
    assinada para um checkout)
    - Ou delegação dessa verificação a um fornecedor de tecnologia (como o MPP).
  - Conclusão do Checkout com o Merchant Payment Processor usando o hash do
    Checkout Mandate e o `payment_token` (com escopo limitado ao Payment
    Mandate).
    - Ou implementação do próprio papel de MPP.
  - Geração de um [Checkout Receipt](checkout_mandate.md#checkout-receipt)
    assinado com o status adequado e retorno ao Shopping Agent.

Alguns exemplos de como o papel de Merchant pode ser estruturado:

  - Merchant com endpoints UCP.
  - Um Merchant Agent que se comunica via agent-to-agent (a2a) com o Shopping
    Agent e, em seguida, com o backend do Merchant via UCP.
  - Merchant e Merchant Payment Processor combinados.
  - Um Merchant com verificação do Checkout Mandate delegada.
    - Nesse caso, o Merchant entrega o Checkout Mandate a um fornecedor de
      tecnologia para verificação e prossegue se a verificação passar.

### Merchant Payment Processor

O Merchant Payment Processor precisa implementar:

  - Recebimento do payment token enviado pelo Merchant
  - Verificação do [Payment Mandate](payment_mandate.md) (autorização assinada
    para o pagamento) contido no payment token.
  - Geração de um [Payment Receipt](payment_mandate.md#payment-receipt)
    assinado, disponibilizado ao Shopping Agent, ao Credential Provider e à
    Network.
  - Processamento ou verificação do pagamento

### Shopping Agent

O Shopping Agent precisa implementar:

  - Agentic Shopping para determinar a intenção do usuário.
  - Seleção de um meio de pagamento de um Credential Provider.
  - Criação do conteúdo dos Checkout e Payment Mandates.
  - Obtenção dos Checkout e Payment Mandates assinados via uma Trusted Surface.
  - Apresentação do [Payment Mandate](payment_mandate.md) ao Credential
    Provider para obter o payment token. Isso envolve:
    - Selecionar o Mandate adequado no armazenamento.
    - Fazer Key Binding com uma chave do Agent (quando necessário).
    - Minimizar dados por meio de Selective Disclosure.
    - Impedir gasto duplo e gerenciar receipts.
  - Apresentação do [Checkout Mandate](checkout_mandate.md) ao Merchant como
    parte da conclusão do Checkout. Isso envolve:
    - Selecionar o Mandate adequado no armazenamento.
    - Fazer Key Binding com uma chave do Agent (quando necessário).
    - Minimizar dados por meio de Selective Disclosure.
    - Impedir gasto duplo e gerenciar receipts.
  - Recebimento de Receipts e tratamento de sucesso e erro.

### Credential Provider

O Credential Provider precisa implementar:

  - Fornecimento de meios de pagamento ao Shopping Agent.
  - Verificação do [Payment Mandate](payment_mandate.md).
  - Obtenção do payment token junto à network usando o Payment Mandate, ou início do envio de fundos ao merchant.
  - Liberação do payment token ou do número de referência do envio de fundos.
  - Recebimento e armazenamento do
    [Payment Receipt](payment_mandate.md#payment-receipt).

Exemplos de como o papel de Credential Provider pode ser implementado:

  - Uma Wallet digital do usuário, ou uma payment network, à qual o Shopping Agent se conecta.
  - Um repositório de meios de pagamento fornecido diretamente pelo Shopping Agent.
  - Um repositório de meios de pagamento fornecido pelo Merchant.

### Trusted Surface

A Trusted Surface representa uma interface considerada confiável por todas as
partes para obter autorização e consentimento do usuário final. Ela é
responsável por:

  - Exibir ao usuário o conteúdo dos Checkout e Payment Mandates.
  - Obter a autorização e o consentimento do usuário.
  - Criar Checkout e Payment Mandates assinados e delegá-los ao
    Shopping Agent.

Esse papel pode ser desempenhado por várias entidades diferentes. Alguns
exemplos:

  - Uma parte determinística da aplicação do Shopping Agent.
  - Uma User Wallet independente, ou uma aplicação do Issuer.
  - User Agents confiáveis (como plataformas móveis ou navegadores).

## Identificação de agentes

O AP2 foi projetado para restringir o comportamento dos Agents sem exigir que
eles sejam confiáveis por natureza. Ao implementar um Commerce Protocol,
Merchants ou Trusted Surfaces MAY (opcional) querer trabalhar apenas com Agents
confiáveis. Esses detalhes ficam a cargo da camada do Commerce Protocol.

## Hashes

Ao calcular hashes, é importante usar a mesma representação. Isso normalmente é
feito usando a representação em base64url das estruturas JSON. Para a resolução
de disputas, isso significa armazenar os SD-JWTs dos Mandates, com suas
disclosures, na serialização compacta. Isso permite calcular facilmente o
`sd_hash`, o `checkout_hash` e o `reference` do Receipt.

Por consistência, o mesmo algoritmo de hash é exigido para os digests do SD-JWT
e para o `checkout_hash`.

## Chave do agente

Uma parte importante dos fluxos Autonomous é a chave do Agent. Ela é usada para
vincular os open Mandates a uma transação e impedir sua reutilização. Também é
usada para impedir gasto duplo, bloqueando a liberação de closed Mandates
sobrepostos.

Uma forma de implementar isso é por tool calling, em que código determinístico
verifica o closed Mandate criado antes de ele ser assinado. Essa
responsabilidade também pode ser delegada pelo Shopping Agent a um fornecedor de
tecnologia.

## Gerenciamento de Mandates

Como os Mandates têm longa duração, o Shopping Agent SHOULD (recomendado)
oferecer um mecanismo para gerenciar os Mandates ativos (junto com as tarefas
em que estão sendo usados). Limitar a duração dos Mandates ativos e enviar
notificações ao usuário, mesmo na execução autônoma, é importante para manter o
usuário no controle do seu Shopping Agent.

No caso de Trusted Surfaces externas, pode fazer sentido permitir o
gerenciamento de Mandates delegados, mas isso está fora do escopo desta
especificação.
