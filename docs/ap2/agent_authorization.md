# Autorização de agentes

Tradução para pt-BR. Em caso de divergência, vale o texto original em inglês em <https://github.com/google-agentic-commerce/AP2>.

Como os processos dos agentes não são determinísticos, mesmo agentes que se
comportam bem precisam ter o comportamento restringido de forma mais rígida do
que um modelo de autorização comum exigiria de usuários humanos.

Este documento apresenta um modelo de autorização agêntica que deixa claro para
o Verifier (verificador) final o que o usuário aprovou que o agente fizesse.
O AP2 usa esse modelo para o caso de uso de pagamentos, mas o modelo pode ser
aplicado de forma mais geral no futuro.

O processo de autorização é dividido em duas etapas:

  - **Mandate Delegation** (delegação de Mandate): o usuário autoriza um agente
    a executar uma ou mais ações em seu nome. Para isso, o usuário aprova o
    conteúdo do Mandate (autorização assinada que serve de prova de intenção) em
    uma Trusted Surface (interface confiável onde o usuário revisa e assina) e
    delega o Mandate resultante ao agente.
  - **Action Authorization** (autorização de ação): um Verifier exige que o
    agente prove que está autorizado a executar uma ação em nome de um usuário.
    O agente faz isso apresentando ao Verifier um Mandate pertinente. Ao final,
    o Verifier devolve ao agente um Receipt (comprovante assinado).

<div style="display: flex; justify-content: space-around;">
  <figure>
    <img src="../../assets/mandate_delegation_overview.svg" style="width:100%" alt="Diagram illustrating the Mandate Delegation process">
    <figcaption align="center">Mandate Delegation</figcaption>
  </figure>
  <figure>
    <img src="../../assets/action_authorization_overview.svg" style="width:100%" alt="Diagram illustrating the Action Authorization process">
    <figcaption align="center">Action Authorization</figcaption>
  </figure>
</div>

## Delegação de Mandate

A delegação de Mandate é feita assim:

  - O agente cria o conteúdo do Mandate que deseja que o usuário autorize.
  - O conteúdo do Mandate é exibido ao usuário em uma Trusted Surface.
  - Após a autorização e o consentimento do usuário, um Mandate é criado e
    devolvido ao agente.
  - O agente armazena o Mandate para uso futuro.

Este documento define os seguintes modelos de delegação de Mandate:

  - User Credential (credencial do usuário)
  - Trusted Agent Provider (provedor do agente, confiável para o Verifier)

A abordagem de User Credential usa um Issuer (emissor) externo ao agente, no
qual o Verifier confia para garantir a Trusted Surface. A vantagem é que uma
única User Credential pode delegar Mandates a vários agentes diferentes, sem
que o Verifier precise ter uma relação de confiança explícita com cada agente.

A abordagem de Trusted Agent Provider faz do provedor do agente a parte em que
o Verifier confia. Isso permite um modelo de confiança mais simples, mas exige
que os Verifiers estabeleçam confiança com cada Agent Provider. Um Agent
Provider também pode ser Issuer de User Credentials, combinando as duas
abordagens.

> NOTA:
> No futuro, outras formas de estabelecer confiança nos Mandates delegados podem
> ser exploradas. O conteúdo do Mandate funciona de forma independente do meio
> usado para estabelecer confiança na sua integridade.
>
> Outros modelos incluem uma chave do usuário com confiança direta, em vez de
> uma credencial completa, como uma passkey ou uma chave atestada por hardware.

### User Credential

Este é um modelo de três partes, que envolve:

  - O Issuer da User Credential
  - A Trusted Surface, como Holder (portadora) da User Credential
  - O agente

Neste modelo, o Verifier confia no Issuer da User Credential para garantir que
a Trusted Surface só construa Mandates depois de obter o consentimento e a
autorização adequados do usuário.

<figure>
  <img src="../../assets/mandate_delegation_user_credential.svg" style="width:100%" alt="Mandate Delegation: User Credential">
  <figcaption align="center">Mandate Delegation: User Credential</figcaption>
</figure>

Antes deste fluxo, o Issuer emite a User Credential para o Holder. O mecanismo
de emissão está fora do escopo deste documento; uma abordagem padronizada pode
ser vista na especificação [OpenID4VCI](#references).

Este modelo faz a criação e a delegação do Mandate como parte da apresentação
de uma VDC (credencial digital verificável) do usuário.

> NOTA:
> Embora este documento especifique o uso de OpenID4VP com SD-JWT VCs, outros formatos de VDC, como [ISO mDocs (ISO18013-5)](#references), e protocolos, como [18013-7 Annex C](#references), podem ser adaptados para cumprir o mesmo papel.

#### Delegação com OpenID4VP

O [OpenID4VP](#references) é um protocolo padronizado para apresentar VDCs de
um holder para um verifier. Um dos recursos do protocolo é `transaction_data`,
que permite que informações adicionais sejam aprovadas e assinadas pelo holder
da credencial digital.

Para fazer a delegação por User Credential com OpenID4VP, o agente monta uma Authorization Request em que o array `transaction_data` contém objetos JSON codificados em base64url. O objeto de delegação do Mandate MUST (obrigatório) conter as seguintes propriedades antes da codificação:

  - **type**: **REQUIRED** (obrigatório). MUST ser o valor de string "*delegate*".
  - **format**: **REQUIRED**. O formato de VDC exigido para o Mandate devolvido.
  - **delegate_payload**: **REQUIRED**. Um array com os payloads do conteúdo do
    Mandate como objetos JSON.
  - **delegate_disclosures**: **OPTIONAL** (opcional). Um array com as
    Selective Disclosures (divulgações seletivas) contidas em `delegate_payload`.

Ao montar a Authorization Response, o `delegate_payload` MUST ser incluído
como parte do Key Binding. Consulte [Delegate SD-JWT](#references) para detalhes.

Os demais campos da Authorization Request MAY (opcional) ser preenchidos
normalmente, por exemplo usando a consulta DCQL para especificar a User
Credential exigida.

É RECOMMENDED (recomendado) usar a Digital Credentials API para delegação com
OpenID4VP, quando disponível, para obter mais segurança e a melhor experiência
de usuário.

Abaixo está um exemplo não normativo de uma Authorization Request do OpenID4VP
para delegar Checkout Mandate e Payment Mandate. As strings em base64url foram truncadas para facilitar a leitura.

```json
{
  "requests": [
    {
      "protocol": "openid4vp-v1-unsigned",
      "data": {
        "response_type": "vp_token",
        "response_mode": "dc_api",
        "nonce": "b5d4e074-dff5-4cd5-a506-f09dd6f2e33a",
        "dcql_query": {
          "credentials": [
            {
              "id": "dpc_credential",
              "format": "dc+sd-jwt",
              "meta": {
                "vct_values": ["com.emvco.dpc"]
              },
              "claims": [
                { "path": ["card_last_four"] },
                { "path": ["card_network_code"] },
                { "path": ["credential_id"] }
              ]
            }
          ]
        },
        "transaction_data": [
          "eyJ0eXBlIjoicGF5bWVudF9jYXJkIiwiY3JlZ...<truncated_payment_card_base64>...5MDBcIn0ifQ==",
          "eyJ0eXBlIjoiZGVsZWdhdGUiLCJmb3JtYXQiO...<truncated_delegate_base64>...aGEtMjU2Il19"
        ],
        "client_metadata": {
          "client_id_scheme": "x509_san_dns",
          "vp_formats": {
            "dc+sd-jwt": {
              "sd-jwt_alg_values": ["ES256"],
              "kb-jwt_alg_values": ["ES256"]
            }
          }
        }
      }
    }
  ]
}
```

**Payloads de `transaction_data` decodificados (informativo)**

O array `transaction_data` contém dois objetos JSON codificados em base64url:

**Índice 0 — Payment Card (dados de interface)**: define a interface de
confirmação exibida ao usuário antes de ele aprovar o pagamento.

```json
{
  "type": "payment_card",
  "credential_ids": ["dpc_credential"],
  "transaction_data_hashes_alg": ["sha-256"],
  "merchant_name": "Generic Merchant",
  "amount": "USD 150.00",
  "additional_info": "{\"title\":\"Please confirm your purchase details...\",\"tableHeader\":[\"Name\",\"Qty\",\"Price\",\"Total\"],\"tableRows\":[[\"Adult Holland Lop Rabbit\",\"1\",\"150.00\",\"150.00\"]],\"footer\":\"Your total is 150.00\"}"
}
```

**Índice 1 — Delegate (Mandates criptográficos)**: vincula o pagamento ao
conteúdo específico do Checkout Mandate e do Payment Mandate por meio de `delegate_payload`.

```json
{
  "type": "delegate",
  "format": "dc+sd-jwt",
  "credential_ids": ["dpc_credential"],
  "transaction_data_hashes_alg": ["sha-256"],
  "delegate_payload": [
    {
      "vct": "mandate.checkout.1",
      "checkout_jwt": "eyJhbGciOiJFUzI1NiIs...<Merchant_Checkout_JWT>",
      "checkout_hash": "3WiKMabE8NRYJgveUbyAZ3pBqRfPrWwGDbOyvbO1eYA",
      "cnf": {
        "jwk": {
          "kty": "EC",
          "crv": "P-256",
          "use": "sig",
          "x": "c09-Eo2PvuO6VrfzLAxTZXBa3ZWkBaa0pR2jcOYKlw",
          "y": "gRETv5wMvNiZJqckokCyDAjIIEg3Y2m77VryMvS75Ww"
        }
      }
    },
    {
      "vct": "mandate.payment.1",
      "transaction_id": "3WiKMabE8NRYJgveUbyAZ3pBqRfPrWwGDbOyvbO1eYA",
      "payment_amount": { "amount": 15000, "currency": "USD" },
      "payee": {
        "id": "merchant_1",
        "name": "Generic Merchant",
        "website": "https://demo-merchant.example"
      },
      "payment_instrument": {
        "id": "b3f1c8a2-6d4e-4f9a-9e3d-8a7c2f1b9d34",
        "type": "dpc",
        "description": "DPC ···· 4444"
      }
    }
  ]
}
```

Abaixo está uma Authorization Response não normativa do OpenID4VP com os
Checkout Mandate e Payment Mandate assinados pelo usuário. As strings longas foram truncadas para facilitar a leitura.

```json
{
  "protocol": "openid4vp-v1-unsigned",
  "data": {
    "vp_token": {
      "dpc_credential": [
        "eyJhbGci...<truncated_issuer_jwt>...jA~WyJiWk5w...<truncated_disclosure_1>...Q~WyJCdThH...<truncated_disclosure_2>...Q~WyJNUThs...<truncated_disclosure_3>...Q~eyJ0eXAi...<truncated_key_binding_jwt>...jZ"
      ]
    }
  }
}
```

O `dpc_credential` é um SD-JWT separado por `~`. Os componentes decodificados são:

**Payload principal do SD-JWT (credencial do Issuer)**

```json
{
  "iss": "https://digital-credentials.dev",
  "vct": "com.emvco.dpc",
  "iat": 1683000000,
  "exp": 1883000000,
  "_sd_alg": "sha-256",
  "_sd": [
    "0ygSIMbyCz_SAL7CrZeDg_C3AnqJVgf35I1t1ie0RZs",
    "1ipSejAAw_lASOeNsGbj3R_3MZNRtalgU9MYvc73Z5g",
    "3d_ksLaY7NAyu9PQZodRB4XsqF2jquCsl2avOlnWCn8",
    "PBhW42ATJqcs3_odVhHuTGEDhN7idDmZMLLORR-lAec"
  ],
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "8jBWriuJBY--u__2jOJfcX4Jj4kEqY4CUX9cf1bQddY",
      "y": "csH2kOGhlemhRRuPUYFKJYZgVqEXQh2JfotRKGRMfLE"
    }
  }
}
```

**Selective Disclosures** (somente os três claims solicitados pelo Merchant são
revelados; os demais campos continuam ocultos nos hashes `_sd` não divulgados):

```json
[
  ["bZNpmTeoL5tYU7gKTVkTUA", "card_last_four", "4444"],
  ["Bu8Gie949nAgBdL6B657Mw", "card_network_code", "ACME"],
  ["MQ8lrNkAwYlavMT8own4DA", "credential_id", "b3f1c8a2-6d4e-4f9a-9e3d-8a7c2f1b9d34"]
]
```

Várias delegações de Mandate MAY ser solicitadas em uma única Authorization
Request, com vários elementos no array `delegate_payload`.

### Trusted Agent Provider

Neste modelo, os Verifiers confiam diretamente no Agent Provider para construir
Mandates somente depois de obter o consentimento e a autorização adequados do
usuário. Este modelo não exige uma credencial emitida previamente. As etapas
são as seguintes:

<figure>
  <img src="../../assets/mandate_delegation_trusted_agent_provider.svg" style="width:100%" alt="Mandate Delegation: Trusted Agent Provider">
  <figcaption align="center">Mandate Delegation: Trusted Agent Provider</figcaption>
</figure>

  - O agente constrói o conteúdo do Mandate e o envia a uma Trusted Surface
    controlada pelo Agent Provider.
      - *Por exemplo, outra parte, determinística, da aplicação do provedor.*
  - A Trusted Surface do Agent Provider exibe o conteúdo do Mandate ao usuário
    e obtém a autorização e o consentimento necessários.
  - O Agent Provider usa uma chave de assinatura armazenada com segurança para criar o Mandate.
      - *Por exemplo, a Trusted Surface se comunica com o backend do Agent
        Provider para que o Mandate seja assinado.*

O Agent Provider MUST garantir que o agente não consiga acessar a chave de
assinatura do Agent Provider nem usá-la sem a Trusted Surface. Consulte
Security and Privacy Considerations para mais detalhes sobre os riscos.

Abaixo está um exemplo não normativo de um Agent Provider criando um Checkout
Mandate como payload `sd-jwt-vc`.

*Payload de nível superior decodificado:*
```json
{
  "iss": "https://agent-provider.example.com",
  "vct": "com.example.agent_mandate",
  "iat": 1777326189,
  "_sd_alg": "sha-256",
  "delegate_payload": [
    { "...": "4UrKesfj0IT5_OE7zLYlXHkAwPbC3JvJgIxku3uq0EE" }
  ]
}
```

*Disclosure decodificada (o open Mandate):*
O hash que termina em `uq0EE` revela o Mandate. Observe que os itens aceitáveis e os Merchants permitidos também ficam ocultos atrás de hashes dentro do array de constraints:
```json
[
  "8rGxzvzfSEW7fw4nb_dYx_w",
  {
    "vct": "mandate.checkout.open.1",
    "cnf": { "jwk": { "crv": "P-256", "kty": "EC", "x": "7MAQoKtK...", "y": "i3OUjGXe..." } },
    "iat": 1777326189,
    "exp": 1777329789,
    "constraints": [
      {
        "type": "checkout.line_items",
        "items": [
          {
            "id": "line_1",
            "quantity": 1,
            "acceptable_items": [
              { "...": "LqZRRzN7nzxJCVf0kP5OvvWvits5CcATHkoq_xGoz8s" }
            ]
          }
        ]
      },
      {
        "type": "checkout.allowed_merchants",
        "allowed": [
          { "...": "UZSGFNQpapJSRQLCeVDfqGzfMCUiJvLL80_kcDai_OI" }
        ]
      }
    ]
  }
]
```

*Disclosures decodificadas (itens de array aninhados):*
O agente pode divulgar seletivamente o item de linha e o Merchant específicos autorizados pelo array de constraints acima:
```json
[
  "vK5dz2nnVpgtoC9dZy9uHw",
  {
    "id": "supershoe_limited_edition_gold_sneaker_womens_9_0",
    "title": "SuperShoe Limited Edition Gold"
  }
]
```
```json
[
  "NAhMECHMBjd978UDQqsAYA",
  {
    "id": "merchant_1",
    "name": "Demo Merchant",
    "website": "https://demo-merchant.example"
  }
]
```

## Estrutura do Mandate

Os Mandates formam uma cadeia verificável criptograficamente, que vai do
Mandate original aprovado pelo usuário até o closed Mandate usado para
autorizar a ação de um Verifier específico.

Os Mandates podem estar em dois estados:

  - **Closed**: quando o Mandate está vinculado a uma transação específica com
    um Verifier, para autorizar o agente a executar uma ação. Isso é feito pelo agente ao gerar um Key Binding JWT (prova de posse) com a chave endossada no claim `cnf` do open Mandate.
  - **Open**: quando o Mandate ainda não foi vinculado a uma transação
    específica. Em vez disso, ele tem um conjunto de constraints (restrições)
    sobre o conteúdo válido do closed Mandate e está vinculado a um agente
    específico autorizado a usar o Mandate.

Open Mandates são necessários para permitir que o agente execute ações
autônomas em nome do usuário, mantendo o comportamento dele restrito de forma
adequada.

<figure>
  <img src="../../assets/mandate_chain_example.svg" style="width:800px" alt="Examples of open and closed Mandate Chains">
  <figcaption align="center">Example: Mandate Chains</figcaption>
</figure>

O diagrama acima mostra dois exemplos de um Mandate que fornece autorização
humana para a mesma ação (doX com A). No caso ‘Human Present’, o usuário
assina diretamente o conteúdo de um closed Mandate; no segundo caso, o usuário assina
o conteúdo de um open Mandate. Em seguida, o agente assina o conteúdo de um closed Mandate em nome do usuário
e fornece a cadeia completa de Mandates para demonstrar a autorização.

Como os open Mandates precisam ser vinculados a uma transação específica antes
do uso, eles MUST oferecer suporte a Key Binding criptográfico.

### Mandates com SD-JWT VCs

[SD-JWT](#references)s oferecem uma estrutura prática para proteger JSON criptograficamente e
várias propriedades úteis para Mandates:

  - O mecanismo de Key Binding permite que o agente forneça prova de posse e
    vinculação à transação quando o usuário não está mais presente.
  - A Selective Disclosure pode ser usada para preservar a privacidade do
    usuário e, ao mesmo tempo, dar ao agente flexibilidade de decisão, divulgando
    apenas as partes aplicáveis da constraint.

> NOTA:
> Embora este documento use SD-JWT VCs, outras VDCs, como ISO mDocs, COULD
> (poderiam) ser usadas no lugar.

O conteúdo do Mandate para SD-JWTs contém os seguintes claims:

  - *vct*: **REQUIRED**. Uma String que identifica de forma única o tipo do
    Mandate, além do tipo da credencial.
  - *constraints*: **OPTIONAL**. Um array de objetos extensíveis que
    definem constraints sobre o que pode estar presente no closed Mandate.
      - *type*: **REQUIRED**. Uma String única que identifica esta constraint.
      - Outras propriedades estão presentes conforme o tipo da constraint.
  - *cnf*: **OPTIONAL**. Contém o método de confirmação que identifica a chave de prova de posse, conforme
    definido na [RFC7800](#references). Este claim é **REQUIRED** se o Mandate ainda estiver open.

Outras propriedades MAY ser incluídas no Mandate conforme o tipo do Mandate. Para
um Mandate que ainda está open, é NOT REQUIRED (não obrigatório) ter todos os campos obrigatórios de um
tipo de Mandate específico, mas o closed Mandate resultante MUST incluí-los.
Além disso, qualquer claim de SD-JWT-VC MAY também ser usado.

A especificação AP2 define tipos de Mandate e tipos de constraint para uso com
pagamentos. Novos tipos de Mandate e novos tipos de constraint MAY ser definidos
além desses para atender a outros casos de uso. É RECOMMENDED usar uma
convenção de nomes resistente a colisões, por exemplo um prefixo rDNS
controlado pela entidade que especifica, ou uma URN adequada.

<a id="verification-and-processing-rules"></a>

#### Regras de verificação e processamento

As regras de verificação e processamento de uma cadeia de Mandates SD-JWT são as
seguintes:

  1. Verifique e processe a cadeia SD-JWT conforme o [Delegate SD-JWT](#references).
  2. Extraia os claims do conteúdo do open Mandate e verifique se o conteúdo do
     closed Mandate mantém esses valores sem alteração.
  3. Extraia cada constraint de cada conteúdo de open Mandate e avalie-a em
     relação ao conteúdo do closed Mandate, de acordo com o tipo da constraint.
     - Qualquer constraint desconhecida MUST ser tratada como falha na avaliação.

## Autorização de ação

A autorização de ação acontece entre um agente e um Verifier. Ela é feita
quando um Verifier precisa que o agente prove que tem a autorização adequada
para executar uma ação específica (como concluir uma compra).

A autorização de ação é feita assim:

1.  O Verifier e o agente interagem até que o Verifier precise de uma prova de
    autorização humana vinda do agente.
2.  O Verifier solicita a apresentação de um Mandate que demonstre que o agente
    está autorizado a executar essa ação.
3.  O agente seleciona um Mandate adequado e o apresenta ao Verifier. Se o
    Mandate estiver open, o agente usa a chave endossada por esse Mandate para
    vinculá-lo à transação.
4.  O Verifier verifica a integridade do Mandate e se o conteúdo do Mandate
    permite que o agente execute a ação pretendida.

Ao apresentar um Mandate que contém selective disclosures, o agente MUST
escolher quais disclosures incluir de modo a maximizar a privacidade do usuário
e ainda assim fornecer a autorização.

*Observação: o mecanismo de seleção do Mandate adequado é um detalhe de
implementação do Shopping Agent e está fora do escopo desta especificação.*

O Verifier faz a verificação do Mandate (consulte
[Verificação](#verification-and-processing-rules)).

Ao aceitar ou rejeitar o Mandate, o Verifier MUST devolver um Mandate Receipt
assinado.
Ao receber um Mandate Receipt de sucesso, o agente armazena a tupla
open Mandate–closed Mandate–Mandate Receipt. O agente reduz o escopo do open
Mandate com base no Receipt, o que muitas vezes impede totalmente novas
apresentações.

Um Mandate Receipt é um JWT assinado pelo Verifier com as seguintes propriedades:

  - *iss*: **REQUIRED**. Uma String com o emissor do JWT, que MUST ser o
    Verifier.
  - *result*: **REQUIRED**. Um Enum com valor `["success", "error"]` que
    indica o resultado da autorização da ação.
  - *reference*: **REQUIRED**. Uma String com o hash, codificado em base64url,
    do Mandate recebido. Ao receber uma cadeia de Mandates, é o hash do último
    SD-JWT da cadeia. É calculado da mesma forma que `sd_hash`. O algoritmo
    usado MUST ser o mesmo `_sd_alg` especificado para o SD-JWT, ou `sha-256`
    se não for especificado.
  - *error*: **OPTIONAL**. Uma String com o código que identifica o erro. MUST
    estar presente quando o resultado for `"error"`.
  - *error_description*: **OPTIONAL**. Uma String com a descrição do erro legível por humanos.

Ele MAY conter propriedades adicionais específicas do caso de uso, conforme a
ação autorizada e o tipo de Mandate recebido.

### Erros
Os seguintes erros são definidos para todas as autorizações de ação:

  - `invalid_credential`: devolvido quando o Mandate falha na verificação. É
    um erro terminal.
  - `unresolved_constraint`: devolvido quando o Mandate contém uma constraint
    desconhecida, ou quando o Verifier não consegue verificar se o closed Mandate atende às
    constraints fornecidas. Isso MAY ser usado como sinal para recorrer
    a um closed Mandate aprovado diretamente ou a outros fluxos não
    agênticos.
  - `invalid_mandate`: devolvido quando o Mandate fornecido não aprova a
    ação solicitada. É um erro terminal.
  - `mandates_not_supported`: indica que o Verifier não aceita Mandates para
    aprovar esta ação. Isso MAY ser usado como sinal para recorrer a fluxos
    não agênticos.

<a id="references"></a>

## Referências

### Normativas

- [OpenID4VP]: T. Lodderstedt, K. Yasuda, T. Looker. "[OpenID for Verifiable Presentations](https://openid.net/specs/openid4vp-1_0.html)", OpenID Foundation, 2024.
- [SD-JWT]: D. Fett, B. Campbell, K. Yasuda, M. B. Jones. "[Selective Disclosure for JWTs (SD-JWT)](https://datatracker.ietf.org/doc/rfc9901/)", fevereiro de 2025.
- [Delegate SD-JWT]: G. Oliver. "[Delegate SD-JWT (Individual Draft)](https://github.com/GarethCOliver/gco-delegate-sd-jwt)", 2026.
- [RFC7800]: M. B. Jones, J. Bradley, H. Tschofenig. "[Proof-of-Possession Key Semantics for JSON Web Tokens (JWTs)](https://datatracker.ietf.org/doc/html/rfc7800)", abril de 2016.

### Informativas

- [OpenID4VCI]: T. Lodderstedt, K. Yasuda, T. Looker. "[OpenID for Verifiable Credential Issuance](https://openid.net/specs/openid4vc-issuance-1_0.html)", OpenID Foundation, 2024.
- [ISO18013-5]: ISO/IEC JTC 1/SC 17. "[ISO/IEC 18013-5:2021 Personal identification — ISO-compliant driving licence — Part 5: Mobile driving licence (mDL) application](https://www.iso.org/standard/69084.html)", setembro de 2021.
- [ISO18013-7]: ISO/IEC JTC 1/SC 17. "[ISO/IEC 18013-7:2024 Personal identification — ISO-compliant driving licence — Part 7: Mobile driving licence (mDL) add-on functions](https://www.iso.org/standard/82763.html)", outubro de 2024.
