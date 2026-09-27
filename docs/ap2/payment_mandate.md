# Payment Mandate

Tradução para pt-BR. Em caso de divergência, vale o texto original em inglês em <https://github.com/google-agentic-commerce/AP2>.

O Payment Mandate (autorização assinada pelo usuário para um pagamento) é um
Mandate (autorização assinada que o protocolo usa como prova de intenção) usado
para autorizar o pagamento de um checkout específico.

## Uso

O conteúdo do Payment Mandate é criado pelo Shopping Agent (agente de compras
que age em nome do usuário), exibido ao usuário pela Trusted Surface (interface
confiável onde o usuário revisa e assina) e verificado pelo Credential Provider
(provedor da credencial de pagamento), pela rede de pagamento e pelo Merchant
Payment Processor (processador de pagamentos do lojista).

## Tipo

Um closed Payment Mandate (mandate com o pagamento final definido) MUST
(obrigatório) usar o valor `mandate.payment.1` no claim `vct`, e um open Payment
Mandate (mandate com constraints, emitido antes de o pagamento final existir)
MUST usar o valor `mandate.payment.open.1`.

Consulte [Mandate Versioning](specification.md#mandate-versioning) para saber
como funciona o sufixo de versão.

## Schema do Mandate

O closed Payment Mandate segue o schema abaixo:

{{ schema_fields('payment_mandate', 'ap2', show_sd=True) }}

O open Payment Mandate MAY (opcional) incluir qualquer propriedade do closed
Payment Mandate.

### Constraints do Payment Mandate

As constraints (restrições que o pagamento final deve atender) abaixo são
definidas neste documento para Payment Mandates:

- **Agent Recurrence:** define as condições para o agente reutilizar este
  Payment Mandate várias vezes.
- **Allowed Payee:** restringe o recebedor a um de um conjunto de Merchants
  possíveis.
- **Allowed Payment Instrument:** restringe o instrumento de pagamento a um de
  um conjunto de instrumentos de pagamento possíveis.
- **Allowed Payment Initiation Service Provider (PISP):** restringe o PISP
  (provedor de serviço de iniciação de pagamento) a um de um conjunto de PISPs
  possíveis.
- **Amount Range:** restringe o valor a uma faixa.
- **Budget:** define um limite de valor total. Deve ser usada com a constraint
  Agent Recurrence.
- **Reference:** restringe o Payment Mandate ao open Checkout Mandate associado
  e aos Checkout Mandates encadeados a partir dele.
- **Execution Date:** restringe a data de execução a um intervalo específico.

### Recorrência pelo agente

**Tipo**: `payment.agent_recurrence`

**Descrição**: define as condições para o agente reutilizar este Payment Mandate várias vezes.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/agent_recurrence') }}

**Avaliação**:
Avaliar o orçamento exige registrar as apresentações anteriores de Payment
Mandates associados a este open Payment Mandate. Esta constraint é avaliada como
verdadeira se o Payment Mandate atual estiver separado no tempo da apresentação
anterior o suficiente para atender à definição de `frequency`, e se o limite
`max_occurrences` for maior ou igual ao número atual de ocorrências.

**Exemplo**
```json
{
  "type": "payment.agent_recurrence",
  "frequency": "MONTHLY",
  "max_occurrences": 12
}
```

### Recebedores permitidos

**Tipo**: `payment.allowed_payees`

**Descrição**: define o conjunto de recebedores possíveis para este Payment
Mandate.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/allowed_payees') }}



**Avaliação**:
A propriedade `payee` do Payment Mandate MUST estar presente no array
`allowed`.

**Exemplo**
```json
{
  "type": "payment.allowed_payees",
  "allowed": [
    {
      "name": "Merchant Choice",
      "website": "https://merchant-choice.com"
    }
  ]
}
```

### Instrumentos de pagamento permitidos

**Tipo**: `payment.allowed_payment_instruments`

**Descrição**: define o conjunto de instrumentos de pagamento possíveis para
este Payment Mandate.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/allowed_payment_instruments') }}



**Avaliação**:
A propriedade `payment_instrument` do Payment Mandate MUST estar presente no
array `allowed`.

**Exemplo**
```json
{
  "type": "payment.allowed_payment_instruments",
  "allowed": [
    {
      "id": "abe3c...",
      "type": "card",
      "description": "network ··· 1234"
    },
    {
      "id": "zde4d...",
      "type": "UPI",
      "description": "user****@bankname"
    },
  ]
}
```

### Provedores de serviço de iniciação de pagamento (PISPs) permitidos

**Tipo**: `payment.allowed_pisps`

**Descrição**: define o conjunto de Payment Initiation Service Providers
(PISPs) autorizados a intermediar a transação.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/allowed_pisps') }}

**Avaliação**: o PISP que intermedia a transação MUST estar presente no array
`allowed`.

**Exemplo**
```json
{
  "type": "payment.allowed_pisps",
  "allowed": [
    {
      "legal_name": "Example Payment Services Ltd.",
      "brand_name": "ExamplePay",
      "domain_name": "examplepay.com"
    }
  ]
}
```

### Faixa de valor

**Tipo**: `payment.amount_range`

**Descrição**: define a faixa válida em que o valor final deve estar.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/amount_range') }}

**Avaliação**:

A propriedade `payment_amount` do Payment Mandate MUST estar dentro da faixa definida
por `min` e `max`. A propriedade `currency` do Payment Mandate MUST ser igual à
propriedade `currency` desta constraint.

**Exemplo**
```json
{
  "type": "payment.amount_range",
  "max": 100.50,
  "min": 10.00,
  "currency": "USD"
}
```

### Orçamento

**Tipo**: `payment.budget`

**Descrição**: define o valor total máximo que pode ser gasto ao usar a
constraint `payment.agent_recurrence`.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/budget') }}

**Avaliação**:
Avaliar o orçamento exige registrar o valor total gasto com este Payment
Mandate. Para esta constraint ser avaliada como verdadeira, o valor solicitado
somado ao total dos valores de closed Payment Mandates anteriores MUST ser
menor ou igual a `max`. Após a aprovação, o valor MUST ser somado ao total
acumulado para avaliações futuras.

**Exemplo**
```json
{
  "type": "payment.budget",
  "max": 1000.00,
  "currency": "USD"
}
```

### Referência

**Tipo**: `payment.reference`

**Descrição**: restringe este Payment Mandate ao uso com um Checkout Mandate
específico (e os closed Mandates associados a ele).

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/payment_reference') }}

**Avaliação**:
O Checkout Mandate do pedido aprovado MUST conter, na sua cadeia de delegação,
um open Checkout Mandate com hash correspondente. O algoritmo de hash usado MUST
ser o algoritmo `_sd_alg` do SD-JWT (JWT com divulgação seletiva) em que esta
constraint está, ou `sha-256` se não estiver definido.

**Exemplo**
```json
{
  "type": "payment.reference",
  "conditional_transaction_id": "A4wG4B..."
}
```

### Data de execução

**Tipo**: `payment.execution_date`

**Descrição**: define a janela de tempo válida para a execução do pagamento.

**Propriedades**:

{{ schema_fields('open_payment_mandate', 'ap2', show_sd=True, pointer='#/$defs/execution_date') }}

**Avaliação**:
O `execution_date` do Payment Mandate MUST ser posterior ou igual a
`not_before` (se presente) e anterior ou igual a `not_after`
(se presente).

**Exemplo**
```json
{
  "type": "payment.execution_date",
  "not_before": "2026-03-31T00:00:00Z",
  "not_after": "2026-04-30T23:59:59Z"
}
```

## Payment Receipt

{{ schema_fields('payment_receipt', 'ap2', show_sd=True) }}

## Exemplos

### SD-JWT do open Payment Mandate com disclosures

```json
{
  "issuer_signed_jwt": {
    "header": {
      "alg": "ES256",
      "typ": "example+sd-jwt",
      "kid": "agent-provider-key-1"
    },
    "payload": {
      "delegate_payload": [
        {
          "...": "3YRtZ-lBNhI_YhggShrdHhrSuDPSpwMvJ3VWjUnhDQM"
        }
      ],
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "oEH7i1gyb-zn6awwjy57LvzxkQDfD-8tvlC2XuIkgOA",
      "decoded": [
        "s9WPt2U4GapcJsonyEb6bjg",
        {
          "id": "merchant_1",
          "name": "Demo Merchant",
          "website": "https://demo-merchant.example"
        }
      ]
    },
    {
      "digest": "3YRtZ-lBNhI_YhggShrdHhrSuDPSpwMvJ3VWjUnhDQM",
      "decoded": [
        "ZtKS5FSrIAY6HlGB4Ho7mg",
        {
          "vct": "mandate.payment.open.1",
          "constraints": [
            {
              "type": "payment.amount_range",
              "currency": "USD",
              "max": 20000,
              "min": 0
            },
            {
              "type": "payment.allowed_payees",
              "allowed": [
                {
                  "...": "oEH7i1gyb-zn6awwjy57LvzxkQDfD-8tvlC2XuIkgOA"
                }
              ]
            },
            {
              "type": "payment.reference",
              "conditional_transaction_id": "FzLoxbbtgQGYZxoSM2NJYJtkFTSsdfUBoVEQ12k7JN8"
            }
          ],
          "cnf": {
            "jwk": {
              "crv": "P-256",
              "kty": "EC",
              "x": "QpSyxPQHy38xckypDr54gZ3T42zj9iLtV4koyb5U27c",
              "y": "37HLd7JJinxjJIn8J7HijssoeclbfhdW-gUL7feI9lw"
            }
          },
          "iat": 1777342357,
          "exp": 1777345957
        }
      ]
    }
  ]
}
```

#### Token codificado

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgImtpZCI6ICJhZ2VudC1wcm92aWRlci1rZXktMSJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIjNZUnRaLWxCTmhJX1loZ2dTaHJkSGhyU3VEUFNwd012SjNWV2pVbmhEUU0ifV0sICJfc2RfYWxnIjogInNoYS0yNTYifQ.ZQ_5x2hYLusuUNAA2OJloeS2w3fxZRCsSvcU-wg9fK7nlMmsbpK6EPlntD8oHq5waegxsLmSL51V5hfyaQViMg~WyJzOVdQdDJVNEdhcGNKc255RWI2YmpnIiwgeyJpZCI6ICJtZXJjaGFudF8xIiwgIm5hbWUiOiAiRGVtbyBNZXJjaGFudCIsICJ3ZWJzaXRlIjogImh0dHBzOi8vZGVtby1tZXJjaGFudC5leGFtcGxlIn1d~WyJadEtTNUZTcklBWTZIbEdCNEhvN21nIiwgeyJ2Y3QiOiAibWFuZGF0ZS5wYXltZW50Lm9wZW4uMSIsICJjb25zdHJhaW50cyI6IFt7InR5cGUiOiAicGF5bWVudC5hbW91bnRfcmFuZ2UiLCAiY3VycmVuY3kiOiAiVVNEIiwgIm1heCI6IDIwMDAwLCAibWluIjogMH0sIHsidHlwZSI6ICJwYXltZW50LmFsbG93ZWRfcGF5ZWVzIiwgImFsbG93ZWQiOiBbeyIuLi4iOiAib0VIN2kxZ3liLXpuNmF3d2p5NTdMdnp4a1FEZkQtOHR2bEMyWHVJa2dPQSJ9XX0sIHsidHlwZSI6ICJwYXltZW50LnJlZmVyZW5jZSIsICJjb25kaXRpb25hbF90cmFuc2FjdGlvbl9pZCI6ICJGekxveGJidGdRR1laeG9TTTJOSllKdGtGVFNzZGZVQm9WRVExMms3Sk44In1dLCAiY25mIjogeyJqd2siOiB7ImNydiI6ICJQLTI1NiIsICJrdHkiOiAiRUMiLCAieCI6ICJRcFN5eFBRSHkzOHhja3l2RHI1NGdaM1Q0MnpqOWlMdFY0a295YjVVMjdjIiwgInkiOiAiMzdITGQ3SkppbnhqSkluOEo3SGlqc3NvZWNCbGZoZFctZ1VMN2ZlSTlsdyJ9fSwgImlhdCI6IDE3NzczNDIzNTcsICJleHAiOiAxNzc3MzQ1OTU3fV0~
```

### SD-JWT do closed Payment Mandate com disclosures

```json
{
  "issuer_signed_jwt": {
    "header": {
      "alg": "ES256",
      "typ": "kb+sd-jwt"
    },
    "payload": {
      "delegate_payload": [
        {
          "...": "G2DuU6IjyDkD-9ItStdsUo48C5uJqDs1E9Hf5GT3TgM"
        }
      ],
      "iat": 1777342370,
      "aud": "credential-provider",
      "nonce": "a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3",
      "sd_hash": "uixoHemmfrrCSbPREo9j-ziLuMkqExsPeWrwA-PK0Ck",
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "G2DuU6IjyDkD-9ItStdsUo48C5uJqDs1E9Hf5GT3TgM",
      "decoded": [
        "FW6McBJImqODuhQlpI4Idw",
        {
          "vct": "mandate.payment.1",
          "transaction_id": "NivWhuqfzcvZNapvIEJ2-3tsdQLkiuIcye2g46WVgX8",
          "payee": {
            "id": "merchant_1",
            "name": "Demo Merchant",
            "website": "https://demo-merchant.example"
          },
          "payment_amount": {
            "amount": 19900,
            "currency": "USD"
          },
          "payment_instrument": {
            "id": "stub",
            "type": "card",
            "description": "Card ••••4242"
          }
        }
      ]
    }
  ]
}
```

#### Token codificado

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImtiK3NkLWp3dCJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIkcyRHVVNklqeURrRC05SXRTdGRzVW80OEM1dUpxRHMxRTlIZjVHVDNUZ00ifV0sICJpYXQiOiAxNzc3MzQyMzcwLCAiYXVkIjogImNyZWRlbnRpYWwtcHJvdmlkZXIiLCAibm9uY2UiOiAiYThiN2M2ZDVlNGYzYTJiMWMwZDllOGY3YTZiNWM0ZDMiLCAic2RfaGFzaCI6ICJ1aXhvSGVtbWZyckNTYlBSRW85ai16aUx1TWtxRXhzUGVXcndBLVBLMENrIiwgIl9zZF9hbGciOiAic2hhLTI1NiJ9.TgI6w9zeL993uzAYE9fnAJXjnrpliDY5DpDKTSQoioH3msapVIz0Ex23ncQXwmsSmT3xOqkSpigQD1EYKck-dQ~WyJmVzZNY0JKSW1xT0R1aFFscEk0SWR3IiwgeyJ2Y3QiOiAibWFuZGF0ZS5wYXltZW50LjEiLCAidHJhbnNhY3Rpb25faWQiOiAiTml2V2h1cWZ6Y3ZaTmFwdklFSjItM3RzZFFMa2l1SWN5ZTJnNDZXVmdYOCIsICJwYXllZSI6IHsiaWQiOiAibWVyY2hhbnRfMSIsICJuYW1lIjogIkRlbW8gTWVyY2hhbnQiLCAid2Vic2l0ZSI6ICJodHRwczovL2RlbW8tbWVyY2hhbnQuZXhhbXBsZSJ9LCAicGF5bWVudF9hbW91bnQiOiB7ImFtb3VudCI6IDE5OTAwLCAiY3VycmVuY3kiOiAiVVNEIn0sICJwYXltZW50X2luc3RydW1lbnQiOiB7ImlkIjogInN0dWIiLCAidHlwZSI6ICJjYXJkIiwgImRlc2NyaXB0aW9uIjogIkNhcmQgXHUyMDIyXHUyMDIyXHUyMDIyNDI0MiJ9fV0~
```

### Open Payment Mandate encadeado com um closed Payment Mandate após o processamento do Delegate SD-JWT.

```json
{
  "issuer_signed_jwt": {
    "header": {
      "alg": "ES256",
      "typ": "example+sd-jwt",
      "kid": "agent-provider-key-1"
    },
    "payload": {
      "delegate_payload": [
        {
          "...": "3YRtZ-lBNhI_YhggShrdHhrSuDPSpwMvJ3VWjUnhDQM"
        }
      ],
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "oEH7i1gyb-zn6awwjy57LvzxkQDfD-8tvlC2XuIkgOA",
      "decoded": [
        "s9WPt2U4GapcJsonyEb6bjg",
        {
          "id": "merchant_1",
          "name": "Demo Merchant",
          "website": "https://demo-merchant.example"
        }
      ]
    },
    {
      "digest": "3YRtZ-lBNhI_YhggShrdHhrSuDPSpwMvJ3VWjUnhDQM",
      "decoded": [
        "ZtKS5FSrIAY6HlGB4Ho7mg",
        {
          "vct": "mandate.payment.open.1",
          "constraints": [
            {
              "type": "payment.amount_range",
              "currency": "USD",
              "max": 20000,
              "min": 0
            },
            {
              "type": "payment.allowed_payees",
              "allowed": [
                {
                  "...": "oEH7i1gyb-zn6awwjy57LvzxkQDfD-8tvlC2XuIkgOA"
                }
              ]
            },
            {
              "type": "payment.reference",
              "conditional_transaction_id": "FzLoxbbtgQGYZxoSM2NJYJtkFTSsdfUBoVEQ12k7JN8"
            }
          ],
          "cnf": {
            "jwk": {
              "crv": "P-256",
              "kty": "EC",
              "x": "QpSyxPQHy38xckypDr54gZ3T42zj9iLtV4koyb5U27c",
              "y": "37HLd7JJinxjJIn8J7HijssoeclbfhdW-gUL7feI9lw"
            }
          },
          "iat": 1777342357,
          "exp": 1777345957
        }
      ]
    }
  ]
}
{
  "issuer_signed_jwt": {
    "header": {
      "alg": "ES256",
      "typ": "kb+sd-jwt"
    },
    "payload": {
      "delegate_payload": [
        {
          "...": "G2DuU6IjyDkD-9ItStdsUo48C5uJqDs1E9Hf5GT3TgM"
        }
      ],
      "iat": 1777342370,
      "aud": "credential-provider",
      "nonce": "a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3",
      "sd_hash": "uixoHemmfrrCSbPREo9j-ziLuMkqExsPeWrwA-PK0Ck",
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "G2DuU6IjyDkD-9ItStdsUo48C5uJqDs1E9Hf5GT3TgM",
      "decoded": [
        "FW6McBJImqODuhQlpI4Idw",
        {
          "vct": "mandate.payment.1",
          "transaction_id": "NivWhuqfzcvZNapvIEJ2-3tsdQLkiuIcye2g46WVgX8",
          "payee": {
            "id": "merchant_1",
            "name": "Demo Merchant",
            "website": "https://demo-merchant.example"
          },
          "payment_amount": {
            "amount": 19900,
            "currency": "USD"
          },
          "payment_instrument": {
            "id": "stub",
            "type": "card",
            "description": "Card ••••4242"
          }
        }
      ]
    }
  ]
}
```

#### Token codificado

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgImtpZCI6ICJhZ2VudC1wcm92aWRlci1rZXktMSJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIjNZUnRaLWxCTmhJX1loZ2dTaHJkSGhyU3VEUFNwd012SjNWV2pVbmhEUU0ifV0sICJfc2RfYWxnIjogInNoYS0yNTYifQ.ZQ_5x2hYLusuUNAA2OJloeS2w3fxZRCsSvcU-wg9fK7nlMmsbpK6EPlntD8oHq5waegxsLmSL51V5hfyaQViMg~WyJzOVdQdDJVNEdhcGNKc255RWI2YmpnIiwgeyJpZCI6ICJtZXJjaGFudF8xIiwgIm5hbWUiOiAiRGVtbyBNZXJjaGFudCIsICJ3ZWJzaXRlIjogImh0dHBzOi8vZGVtby1tZXJjaGFudC5leGFtcGxlIn1d~WyJadEtTNUZTcklBWTZIbEdCNEhvN21nIiwgeyJ2Y3QiOiAibWFuZGF0ZS5wYXltZW50Lm9wZW4uMSIsICJjb25zdHJhaW50cyI6IFt7InR5cGUiOiAicGF5bWVudC5hbW91bnRfcmFuZ2UiLCAiY3VycmVuY3kiOiAiVVNEIiwgIm1heCI6IDIwMDAwLCAibWluIjogMH0sIHsidHlwZSI6ICJwYXltZW50LmFsbG93ZWRfcGF5ZWVzIiwgImFsbG93ZWQiOiBbeyIuLi4iOiAib0VIN2kxZ3liLXpuNmF3d2p5NTdMdnp4a1FEZkQtOHR2bEMyWHVJa2dPQSJ9XX0sIHsidHlwZSI6ICJwYXltZW50LnJlZmVyZW5jZSIsICJjb25kaXRpb25hbF90cmFuc2FjdGlvbl9pZCI6ICJGekxveGJidGdRR1laeG9TTTJOSllKdGtGVFNzZGZVQm9WRVExMms3Sk44In1dLCAiY25mIjogeyJqd2siOiB7ImNydiI6ICJQLTI1NiIsICJrdHkiOiAiRUMiLCAieCI6ICJRcFN5eFBRSHkzOHhja3l2RHI1NGdaM1Q0MnpqOWlMdFY0a295YjVVMjdjIiwgInkiOiAiMzdITGQ3SkppbnhqSkluOEo3SGlqc3NvZWNCbGZoZFctZ1VMN2ZlSTlsdyJ9fSwgImlhdCI6IDE3NzczNDIzNTcsICJleHAiOiAxNzc3MzQ1OTU3fV0~~eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImtiK3NkLWp3dCJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIkcyRHVVNklqeURrRC05SXRTdGRzVW80OEM1dUpxRHMxRTlIZjVHVDNUZ00ifV0sICJpYXQiOiAxNzc3MzQyMzcwLCAiYXVkIjogImNyZWRlbnRpYWwtcHJvdmlkZXIiLCAibm9uY2UiOiAiYThiN2M2ZDVlNGYzYTJiMWMwZDllOGY3YTZiNWM0ZDMiLCAic2RfaGFzaCI6ICJ1aXhvSGVtbWZyckNTYlBSRW85ai16aUx1TWtxRXhzUGVXcndBLVBLMENrIiwgIl9zZF9hbGciOiAic2hhLTI1NiJ9.TgI6w9zeL993uzAYE9fnAJXjnrpliDY5DpDKTSQoioH3msapVIz0Ex23ncQXwmsSmT3xOqkSpigQD1EYKck-dQ~WyJmVzZNY0JKSW1xT0R1aFFscEk0SWR3IiwgeyJ2Y3QiOiAibWFuZGF0ZS5wYXltZW50LjEiLCAidHJhbnNhY3Rpb25faWQiOiAiTml2V2h1cWZ6Y3ZaTmFwdklFSjItM3RzZFFMa2l1SWN5ZTJnNDZXVmdYOCIsICJwYXllZSI6IHsiaWQiOiAibWVyY2hhbnRfMSIsICJuYW1lIjogIkRlbW8gTWVyY2hhbnQiLCAid2Vic2l0ZSI6ICJodHRwczovL2RlbW8tbWVyY2hhbnQuZXhhbXBsZSJ9LCAicGF5bWVudF9hbW91bnQiOiB7ImFtb3VudCI6IDE5OTAwLCAiY3VycmVuY3kiOiAiVVNEIn0sICJwYXltZW50X2luc3RydW1lbnQiOiB7ImlkIjogInN0dWIiLCAidHlwZSI6ICJjYXJkIiwgImRlc2NyaXB0aW9uIjogIkNhcmQgXHUyMDIyXHUyMDIyXHUyMDIyNDI0MiJ9fV0~
```

## Tipos comuns

### Amount

{{ schema_fields('types/amount', 'ap2', show_sd=True) }}

### Merchant

{{ schema_fields('types/merchant', 'ap2', show_sd=True) }}

### PaymentInstrument

{{ schema_fields('types/payment_instrument', 'ap2', show_sd=True) }}

### Pisp

{{ schema_fields('types/pisp', 'ap2', show_sd=True) }}
