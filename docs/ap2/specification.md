# Agentic Payment Protocol (v0.2)

Tradução para pt-BR. Em caso de divergência, vale o texto original em inglês em <https://github.com/google-agentic-commerce/AP2>.

O Agentic Payment Protocol (AP2) define um protocolo para proteger transações
de pagamento realizadas por agentes. Ele usa o
[modelo de Agent Authorization](agent_authorization.md).

Esta especificação descreve:

-   Os diferentes papéis das entidades no AP2.
-   As responsabilidades de verificação de cada papel.
-   Um [Checkout Mandate](checkout_mandate.md) (autorização assinada para um
    checkout) e um [Receipt](checkout_mandate.md#checkout-receipt) (comprovante
    assinado do resultado) para proteger *o que* está sendo comprado.
-   Um [Payment Mandate](payment_mandate.md) (autorização assinada para o
    pagamento) vinculado e seu [Receipt](payment_mandate.md#payment-receipt)
    para o *pagamento* do Checkout.
-   Como os Checkout e Payment Mandates podem ser usados como evidência em caso
    de disputa.

O AP2 funciona como um recurso de segurança dentro de um Commerce Protocol. Os
detalhes do Commerce Protocol (por exemplo, APIs de catálogo, atualizações de
checkout e APIs específicas para comunicação entre os papéis) estão fora do
escopo do AP2. O AP2 foi projetado explicitamente para ser compatível com o
Universal Commerce Protocol (UCP) e se integra diretamente a ele.

Há exemplos ilustrativos dos fluxos
[Human Present ('direct')](flows.md#human-present) e
[Human Not Present ('autonomous')](flows.md#human-not-present).

## Papéis

O AP2 considera cinco papéis, com responsabilidades diferentes do ponto de vista
de processamento e verificação:

-   **Shopping Agent (SA):** o Shopping Agent é o agente principal, que faz a
    descoberta de produtos, monta o checkout e executa a compra.
-   **Credential Provider (CP):** o Credential Provider é a origem das Payment
    Credentials da compra. Ele verifica se o Agent está autorizado a acessar
    essa Payment Credential e limita o escopo da Payment Credential de forma
    adequada.
-   **Merchant (M):** o papel de Merchant fornece e conclui o Checkout. Ele
    verifica se o Shopping Agent está aprovado para comprar esses itens e
    responde pela integridade do estoque, dos preços e de descontos do
    merchant.
-   **Merchant Payment Processor (MPP):** o papel de Merchant Payment Processor
    processa os pagamentos das compras. Ele verifica se a Payment Credential
    compartilhada pelo Credential Provider foi autorizada a pagar por esta
    instância de Checkout.
-   **Trusted Surface (TS):** o papel de Trusted Surface é uma interface
    considerada confiável para obter o consentimento informado do usuário para
    uma Intent antes de criar um Mandate assinado pelo usuário.

> Observação: embora o AP2 defina cinco papéis, uma única entidade pode
> desempenhar vários papéis (ou até todos). Nesse caso, ela assume todas as
> responsabilidades de cada papel que desempenha.

Os papéis MAY (podem, opcional) sempre delegar suas responsabilidades a outra
parte.

## Agentic e Non-Agentic

Muitos desses papéis podem ser considerados Agentic ou Non-Agentic. Um papel é
Agentic quando:

-   A comunicação de ou para o papel é tratada por um LLM não determinístico.

Um papel é considerado Non-Agentic se:

-   A comunicação de e para o papel é tratada por código determinístico que
    verifica a autenticidade e a correção.
-   E se nenhum processamento feito pelo papel é delegado a um LLM.

Os seguintes papéis MAY ser agentic ou non-agentic:

-   Merchant
-   Merchant Payment Processor
-   Credential Provider

O seguinte papel MUST (obrigatório) ser non-agentic:

-   Trusted Surface

Espera-se que o seguinte papel seja agentic:

-   Shopping Agent

Quando a comunicação ocorre entre dois papéis non-agentic, a segurança web
padrão basta para garantir a integridade. Porém, quando qualquer um dos papéis é
agentic, o próprio Agent é um potencial atacante. Por isso, são necessários
mecanismos adicionais que evidenciem adulteração para garantir uma comunicação
segura.

O AP2 assume que, no mínimo, o Shopping Agent é agentic. Quando a jornada de
pagamento ocorre diretamente entre duas superfícies non-agentic (por exemplo,
uma Trusted Surface que se comunica diretamente com um Merchant non-agentic),
os modelos de segurança de e-commerce existentes são suficientes.

Quando este documento se refere a validação ou processamento de um papel, isso
MUST ocorrer em código determinístico, seja o papel agentic ou não.

## Mandates

Mandates são o principal meio que o AP2 usa para autorizar agentes. Veja
[Agent Authorization Framework][agent_authorization.md] para uma descrição de
como isso funciona no caso geral.

O AP2 define dois
tipos de Mandate: Checkout Mandate e Payment Mandate.

O conteúdo dos Checkout e Payment Mandates é montado pelo Shopping Agent depois
que ele determina qual tarefa o usuário quer que ele execute. Os detalhes de
como isso é feito estão fora do escopo desta especificação.

Em seguida, o Shopping Agent usa uma Trusted Surface para obter Checkout e
Payment Mandates assinados, que ele usará para autorizar o pagamento e concluir
o Checkout.

### Checkout Mandate

O Checkout Mandate foi projetado para dar ao Merchant prova criptográfica de que
o Shopping Agent está autorizado a comprar o Checkout que montou.

O Checkout Mandate é fornecido pelo Shopping Agent e verificado pelo Merchant.

O Merchant MUST fornecer ao Shopping Agent um JWT assinado pelo merchant
contendo o Checkout. O closed Checkout Mandate é vinculado a esse Checkout JWT
por meio de um hash criptográfico.

Depois que o Merchant aceitar ou rejeitar o Checkout Mandate, ele MUST retornar
um Checkout Receipt.

Para os detalhes completos das estruturas do Checkout Mandate e do Receipt, veja
[Checkout Mandate](checkout_mandate.md).

<a id="mandate-versioning"></a>

### Versionamento de Mandates

Cada tipo de Mandate do AP2 identifica seu schema com a claim `vct`. O valor de
`vct` inclui um sufixo numérico que funciona como número de versão do schema
(por exemplo, `mandate.payment.1`, `mandate.checkout.open.1`). As
implementações MUST corresponder exatamente à string `vct`, incluindo o sufixo
de versão. Uma revisão futura incompatível do schema introduziria um novo
sufixo (por exemplo, `.2`), permitindo distinguir versões antigas e novas sem
ambiguidade.

### Payment Mandate

O Payment Mandate foi projetado para dar ao Credential Provider, à Network e ao
Merchant Payment Processor prova criptográfica de que o Shopping Agent está
autorizado a pagar por um Checkout específico.

O Payment Mandate é fornecido pelo Shopping Agent e verificado pelo Credential
Provider, pela Network e pelo Merchant Payment Processor.

O Payment Mandate é vinculado a um Checkout específico pelo hash criptográfico
do Checkout JWT. Para evitar ataques de rainbow table, o Checkout JWT MUST ser
assinado com um esquema de assinatura digital (por exemplo, ECDSA) e não com
uma assinatura determinística (por exemplo, Ed25519).

Depois que o Merchant Payment Processor aceitar ou rejeitar o Payment Mandate,
um Payment Receipt assinado MUST ser retornado ao Shopping Agent, ao Credential
Provider e, possivelmente, às Networks.

Para os detalhes completos das estruturas do Payment Mandate e do Receipt, veja
[Payment Mandate](payment_mandate.md).

## Modos

Há dois `modes` em que o AP2 pode operar.

-   Human Present (Direct): o usuário vê diretamente o closed Checkout e o
    aprova, junto com o pagamento, de forma explícita.

-   Human Not Present (Autonomous): o usuário vê e aprova um conjunto de
    constraints sobre quais closed Checkout e Payment atenderiam à sua
    intenção. Em seguida, o Shopping Agent monta e aprova um closed Checkout e
    Payment Mandate em nome do usuário usando esses open Mandates.

Os verificadores de Mandates *sempre* recebem um closed Payment Mandate e um
closed Checkout Mandate, qualquer que seja o modo. A diferença está apenas em
como a verificação do Mandate é feita.

No caso Direct, a assinatura dos closed Mandates é validada como vinda
diretamente de um usuário, usando uma User Credential ou uma lista de confiança
de Agent Providers.

No caso Autonomous, os closed Mandates são assinados por uma chave do Agent. A
confiança nessa chave vem de open Mandates assinados pelo usuário ou de uma
lista de confiança de Agent Providers. As constraints desses Mandates permitem
ao verificador confirmar que o Checkout e o Payment correspondem à intenção do
usuário. Apenas as constraints relevantes para os closed Mandates são
compartilhadas com o verificador.

### Direct (Human Present)

Quando o Shopping Agent tem, do Merchant, um Checkout JWT para o closed
Checkout, ele monta o conteúdo dos Checkout e Payment Mandates e o envia a uma
Trusted Surface para exibição ao usuário e assinatura.

Ao receber os Checkout e Payment Mandates, o Shopping Agent encaminha o Payment
Mandate ao Credential Provider (e, possivelmente, à Network) para verificação.
Se a verificação for bem-sucedida, o Shopping Agent recebe uma payment
credential.

A payment credential e um Checkout Mandate são então fornecidos ao Merchant.
O Merchant confere o Checkout com o que criou e inicia o pagamento com o
Merchant Payment Processor, se for uma cobrança iniciada pelo Merchant.

Quando o meio de pagamento envia os fundos ao Merchant (push), o Merchant
recebe a confirmação do envio dos fundos e confirma o recebimento.

Ao final, um Checkout Receipt é retornado ao Shopping Agent, e o Payment
Receipt é retornado ao Shopping Agent, ao Credential Provider e, se aplicável, à
Network.

Veja [Human Present](flows.md#human-present) para um exemplo detalhado.

> Observação: como o usuário aprova o closed Checkout, isso muitas vezes pode
> ser substituído por uma jornada de e-commerce tradicional em que o Merchant e
> a Trusted Surface se comunicam diretamente.

### Autonomous (Human Not Present)

Quando o Shopping Agent precisa operar de forma autônoma, ele cria o conteúdo
de open Checkout e Payment Mandates e os submete à autorização na Trusted
Surface. Esses Mandates MUST incluir a chave pública do agente como claim
`cnf`. Isso é necessário porque eles ainda não estão vinculados a uma transação
específica e, por isso, precisam ter o uso restrito ao Agent. É RECOMMENDED
(recomendado) definir a claim `exp` desses Mandates com o menor valor que
permita ao Shopping Agent concluir a tarefa atribuída.

Depois que o Shopping Agent criar um Checkout adequado, para autorizá-lo o
Shopping Agent MAY assiná-lo com sua Agent Key, em vez de obter aprovação em
uma Trusted Surface. Em seguida, ele MUST fornecer às partes verificadoras
tanto o open Mandate assinado pelo usuário quanto o closed Mandate assinado
pelo agente, como descrito no caso Direct acima.

Shopping Agents MUST NOT (proibido) apresentar novos open Payment ou Checkout
Mandates sem receber um receipt de rejeição do anterior. Isso impede que um
Agent aprove vários Checkouts diferentes usando o mesmo open Mandate.

Para garantir a privacidade do usuário, os Shopping Agents MUST apresentar
apenas as disclosures dos open Mandates necessárias para avaliar os closed
Mandates.

Ao final, um Checkout Receipt é retornado ao Shopping Agent, e o Payment
Receipt é retornado ao Shopping Agent, ao Credential Provider e, se aplicável, à
Network.

Veja [Human Not Present](flows.md#human-not-present) para um exemplo detalhado.

> Observação: na especificação atual, o Shopping Agent precisa determinar os
> Mandates e as Disclosures aplicáveis caso a caso, com base no Checkout. No
> futuro, o uso de uma linguagem de consulta explícita no commerce protocol
> pode facilitar a interoperabilidade prática.

#### Delegação entre agentes

Conceitualmente, é possível usar este protocolo para delegar Mandates de um
Shopping Agent para outro. Isso está fora do escopo da especificação atual.

## Evidência em disputas

Em caso de disputa, o Checkout Mandate e seu Receipt e o Payment Mandate e seu
Receipt podem ser reunidos para fornecer um registro irrefutável da transação.
Os detalhes de como isso é usado na resolução de disputas e os requisitos de
retenção e recuperação estão fora do escopo desta especificação.

O Checkout Mandate e o Receipt MAY ser fornecidos pelos seguintes papéis:

-   Shopping Agent
-   Merchant

O Payment Mandate e o Receipt MAY ser fornecidos pelos seguintes papéis:

-   Shopping Agent
-   Credential Provider
-   Network
-   Merchant Payment Processor

Veja [Verificação: disputa](#dispute) para as regras de verificação.

> Observação: oferecer um método automatizado para obter o Checkout Mandate,
> seja do Shopping Agent ou do Merchant, seria muito útil para o ecossistema. Os
> detalhes estão fora do escopo da versão atual, mas isso seria feito usando o
> `transaction_id` do Payment Mandate como chave da solicitação.

## Verificação

Os papéis a seguir MUST seguir estas regras de verificação ao receber o
Mandate.

> Observação: um papel sempre pode delegar suas responsabilidades a um
> fornecedor de tecnologia. Por exemplo, um Merchant pode pedir que seu
> processador de pagamentos faça as verificações em seu nome. Nesse caso, o
> delegado segue as regras de verificação desse papel.

### Merchant

O Merchant MUST receber um Checkout Mandate adequado de um Shopping Agent antes
de concluir o Checkout.

Ele MUST verificar o Checkout Mandate da seguinte forma:

-   Processar e verificar o Checkout Mandate conforme as
    [regras de verificação e processamento](agent_authorization.md#verification-and-processing-rules).
-   Verificar se o hash do Checkout JWT enviado para aprovação corresponde ao
    valor incluído na claim `checkout_hash`.
-   Se open Checkout Mandates estiverem incluídos, verificar se o closed
    Checkout atende a todas as Constraints, avaliando cada uma delas.

Se qualquer etapa falhar, o Merchant MUST retornar um Checkout Receipt JWT com a
mensagem de erro adequada.

### Credential Provider e Network

O Credential Provider e, se aplicável, a Network MUST receber um Payment Mandate
adequado do Shopping Agent antes de retornar uma payment credential.

Eles MUST verificar o Payment Mandate da seguinte forma:

-   Processar e verificar o Payment Mandate conforme as
    [regras de verificação e processamento](agent_authorization.md#verification-and-processing-rules).
-   Se open Payment Mandates estiverem incluídos, verificar se o closed Payment
    Mandate atende a todas as Constraints.

Se qualquer etapa falhar, eles MUST retornar ao Shopping Agent um Payment
Receipt JWT com o erro adequado.

### Merchant Payment Processor

O Merchant Payment Processor MUST receber uma Payment Credential adequada do
Merchant antes de processar a transação.

O Merchant Payment Processor MUST verificar se a Payment Credential tem escopo
adequado ao Checkout. Uma forma de fazer isso é incluir o closed Payment
Mandate dentro da Payment Credential.

<a id="dispute"></a>

### Disputa

Ao fazer a verificação no momento de uma disputa, as seguintes etapas MUST ser
seguidas para garantir a integridade dos Payment e Checkout Mandates e dos
Receipts.

-   O Checkout Mandate MUST ser verificado conforme as regras de verificação do
    Merchant.
-   O hash do `checkout_jwt` MUST ser calculado de forma independente a partir
    do `checkout_jwt` incluído.
-   O `reference` do Checkout Receipt MUST corresponder ao hash do closed
    Checkout Mandate. Ele é calculado da mesma forma que o `sd_hash`.
-   O Payment Mandate MUST ser verificado conforme a seção
    [Merchant Payment Processor](#merchant-payment-processor), usando o
    `checkout_hash` do Checkout Mandate.
-   O reference do Payment Receipt MUST corresponder ao hash do closed Payment
    Mandate. Ele é calculado da mesma forma que o `sd_hash`.

Depois que todas essas etapas forem concluídas com sucesso, as informações do
Checkout Mandate e do Payment Mandate podem ser usadas como evidência do que o
usuário e cada papel viram.

## Pontos de extensão

O AP2 oferece vários pontos de extensão para se adaptar às necessidades do
Agentic Commerce:

### Constraints de Mandate

Este ponto de extensão serve para restringir o comportamento do Agent e, ao
mesmo tempo, permitir casos de uso autônomos mais complexos. Para definir uma
nova constraint, os seguintes itens MUST ser especificados:

-   Um `type` com definição única.
-   Um Schema, incluindo quais campos permitem divulgação seletiva.
-   O algoritmo de avaliação.

### Objeto de Checkout

O AP2 é agnóstico ao conteúdo do Checkout JWT assinado pelo merchant. Ele foi
criado para ser compatível com Checkout Objects representados logicamente, mas
oferece um ponto de extensão para ser adaptado a outros Checkout Objects. O
próprio UCP também oferece esses pontos de extensão dentro do protocolo, que é
a forma RECOMMENDED de suportar novas jornadas de comércio.

### Meio de pagamento

O AP2 é agnóstico ao meio de pagamento usado. Novos Payment Instruments são
suportados pela definição de um `type` único no objeto JSON Payment Instrument.
Se necessário, propriedades adicionais MAY ser definidas para esse `type`
específico.

### Formatos de Verifiable Digital Credential (VDCs)

O AP2 especifica o uso de `SD-JWT`s para proteger os Payment e Checkout
Mandates. Os Payment e Checkout Mandates poderiam ser protegidos
criptograficamente por outras VDCs, como mencionado em
[Agent Authorization](agent_authorization.md).
