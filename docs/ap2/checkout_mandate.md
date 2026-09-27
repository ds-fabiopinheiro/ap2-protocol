# Checkout Mandate

Tradução para pt-BR. Em caso de divergência, vale o texto original em inglês em <https://github.com/google-agentic-commerce/AP2>.

O Checkout Mandate (autorização assinada pelo usuário para um checkout) é um
Mandate (autorização assinada que o protocolo usa como prova de intenção) usado
para autorizar a conclusão de um checkout.

## Uso

O conteúdo do Checkout Mandate é criado pelo Shopping Agent (agente de compras
que age em nome do usuário), exibido ao usuário pela Trusted Surface (interface
confiável onde o usuário revisa e assina) e verificado pelo Merchant
(lojista). O Merchant cria um objeto Checkout assinado, que é incluído no
conteúdo do closed Checkout Mandate.

## Tipo

Um closed Checkout Mandate (mandate com o checkout final definido) MUST
(obrigatório) usar o valor `mandate.checkout.1` no claim `vct`, e um open
Checkout Mandate (mandate com constraints, emitido antes de o checkout existir)
MUST usar o valor `mandate.checkout.open.1`.

Consulte [Mandate Versioning](specification.md#mandate-versioning) para saber
como funciona o sufixo de versão.

## Schema do Mandate

O closed Checkout Mandate segue o schema abaixo:

{{ schema_fields('checkout_mandate', 'ap2', show_sd=True) }}

`checkout_hash` é o hash, codificado em base64url, do valor de `checkout_jwt`.
O algoritmo usado MUST ser o mesmo do SD-JWT (JWT com divulgação seletiva),
conforme definido pelo claim `_sd_alg` no payload base, ou `sha-256` se esse
claim não estiver presente.

`checkout_jwt` é o JWT assinado pelo Merchant que contém os detalhes do
checkout. Os detalhes do payload estão fora do escopo desta especificação;
quando usado com o [Universal Commerce Protocol](https://ucp.dev), MUST ser o
objeto Checkout.

## Constraints

As constraints (restrições que o checkout final deve atender) abaixo são
definidas neste documento para uso com open Checkout Mandates:

-   **Allowed Merchant:** restringe os Merchants com os quais este Checkout
    Mandate pode ser usado.
-   **Line Items:** define o conjunto válido de itens de linha que devem ser
    incluídos no Checkout Mandate.

### Merchants permitidos

**Tipo**: `checkout.allowed_merchants`

**Descrição**: restringe os Merchants possíveis para este Checkout Mandate.

**Propriedades**:

{{ schema_fields('open_checkout_mandate', 'ap2', show_sd=True,
pointer='#/$defs/allowed_merchants') }}

**Avaliação**: o Merchant MUST estar presente entre os elementos revelados de
`allowed`. Se não estiver presente, ou se `allowed` não tiver nenhum elemento
revelado, a constraint é inválida.

**Exemplo**
```json
{
  "type":  "checkout.allowed_merchants",
  "allowed": [
    {"name": "Merchant Choice", "website": "https://merchant-choice.com" },
    {"name": "Second Merchant", "website": "https://second-merchant.com" },
  ]
}
```

### Itens de linha

**Tipo**: `checkout.line_items`

**Descrição**: define os conjuntos de itens de linha que devem estar presentes
no checkout_jwt.

**Propriedades**:

{{ schema_fields('open_checkout_mandate', 'ap2', show_sd=True,
pointer='#/$defs/line_items') }}

**Avaliação**: esta constraint é atendida quando:

-   Cada entrada de `items` na constraint tem uma quantidade total de itens
    correspondentes no Checkout.
-   Um item corresponde a uma entrada de `items` se o ID dele estiver presente
    nos `acceptable_items` revelados.
-   Nenhuma entrada de `items` nem item do Checkout pode ser usado mais de uma
    vez.

Uma forma de implementar isso é como um problema de fluxo máximo. O grafo é
definido assim:

1.  Crie um nó para cada entrada de `items`.
2.  Crie uma aresta da origem até cada nó de `items`, com capacidade igual à
    quantidade.
3.  Crie um nó para cada ID de item no Checkout.
4.  Crie uma aresta de cada nó de item do Checkout até o sumidouro, com
    capacidade igual à quantidade total desse ID de item no checkout.
5.  Crie uma aresta com capacidade infinita entre cada nó de `items` e cada nó
    de item do Checkout que corresponda aos `acceptable_items` revelados para
    esse item.

A constraint é atendida se o fluxo máximo for igual à quantidade total de
`items` da constraint e à quantidade total de `items` do checkout.

> NOTA: esta avaliação não permite dividir o open Checkout Mandate entre
> vários Checkouts. Extensões futuras de constraints podem adicionar esse
> suporte, mas é preciso considerar como evitar vários pedidos duplicados.

**Exemplo**
```json
{
  "type":  "checkout.line_items",
  "items": [
    {
      "id": "id-shoe-choices",
      "acceptable_items": [
        {"id": "BAB1234", "title": "Red Style"}
        {"id": "FAF1234", "title": "Blue Style"}
      ],
      "quantity": 1
    },
    {
      "id": "id-sock-choices",
      "acceptable_items": [
        {"id": "QRT1234", "title": "The Best Socks"}
      ],
      "quantity": 1
    },
  ]
}
```
Isso seria atendido pelas seguintes combinações:
  - Item: Red Style, Item: The Best Socks
  - Item: Blue Style, Item 3: The Best Socks

Mas seria inválido ter um Checkout contendo:
  - Item: Red Style, Item: Blue Style
  - Item: Red Style
  - Item: Blue Style
  - Item: The Best Socks

## Checkout Receipt

O Checkout Receipt (comprovante assinado do checkout) segue o schema abaixo:

{{ schema_fields('checkout_receipt', 'ap2', show_sd=True) }}

## Exemplos

### SD-JWT do open Checkout Mandate com disclosures

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
          "...": "QtXTJtWqg999CmUWGjHFTWMkRPguDfeK3wGSaInd-dw"
        }
      ],
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "y3aocAD2rhYpJQOUMN016faDFGkTBGEDVl1R1TRHdbw",
      "decoded": [
        "4n3L_-3_Fm2GgyFAF8Ct_g",
        {
          "id": "supershoe_limited_edition_gold_sneaker_womens_9_0",
          "title": "SuperShoe Limited Edition Gold"
        }
      ]
    },
    {
      "digest": "a5UMAdxCk_MRayyVdRhpIAZ0ZhjVLEq1g2BWyruKUwg",
      "decoded": [
        "2zPL6vqLBg2WYAdbW9-1lQ",
        {
          "id": "merchant_1",
          "name": "Demo Merchant",
          "website": "https://demo-merchant.example"
        }
      ]
    },
    {
      "digest": "QtXTJtWqg999CmUWGjHFTWMkRPguDfeK3wGSaInd-dw",
      "decoded": [
        "laAoWKNRuGnwREjJWYJ7pg",
        {
          "vct": "mandate.checkout.open.1",
          "constraints": [
            {
              "type": "checkout.line_items",
              "items": [
                {
                  "id": "line_1",
                  "acceptable_items": [
                    {
                      "...": "y3aocAD2rhYpJQOUMN016faDFGkTBGEDVl1R1TRHdbw"
                    }
                  ],
                  "quantity": 1
                }
              ]
            },
            {
              "type": "checkout.allowed_merchants",
              "allowed": [
                {
                  "...": "a5UMAdxCk_MRayyVdRhpIAZ0ZhjVLEq1g2BWyruKUwg"
                }
              ]
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
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgImtpZCI6ICJhZ2VudC1wcm92aWRlci1rZXktMSJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIlF0WFRKdFdxZzk5OUNtVVdHakhGVFdNa1JQZ3VEZmVLM3dHU2FJbmQtZHcifV0sICJfc2RfYWxnIjogInNoYS0yNTYifQ.HvCGk7ye_c0LN2-NFG13wfyu3LA--rckTPGm36ugO2aRvsded7ngw1py8W3JF7wBpoQnsKr17tNTF3zLeYcoWA~WyI0bjNMXy0zX0ZtMkdneUZBRjhDdF9nIiwgeyJpZCI6ICJzdXBlcnNob2VfbGltaXRlZF9lZGl0aW9uX2dvbGRfc25lYWtlcl93b21lbnNfOV8wIiwgInRpdGxlIjogIlN1cGVyU2hvZSBMaW1pdGVkIEVkaXRpb24gR29sZCJ9XQ~WyIyelBMNnZxTEJnMldZQWRiVzktMWxRIiwgeyJpZCI6ICJtZXJjaGFudF8xIiwgIm5hbWUiOiAiRGVtbyBNZXJjaGFudCIsICJ3ZWJzaXRlIjogImh0dHBzOi8vZGVtby1tZXJjaGFudC5leGFtcGxlIn1d~WyJsYUFvV0tOUnVHbndSRWpKV1lKN3BnIiwgeyJ2Y3QiOiAibWFuZGF0ZS5jaGVja291dC5vcGVuLjEiLCAiY29uc3RyYWludHMiOiBbeyJ0eXBlIjogImNoZWNrb3V0LmxpbmVfaXRlbXMiLCAiaXRlbXMiOiBbeyJpZCI6ICJsaW5lXzEiLCAiYWNjZXB0YWJsZV9pdGVtcyI6IFt7Ii4uLiI6ICJ5M2FvY0FEMnJoWXBKUU9VTU4wMTZmYURGR2tUQkdFRFZsMVIxVFJIZGJ3In1dLCAicXVhbnRpdHkiOiAxfV19LCB7InR5cGUiOiAiY2hlY2tvdXQuYWxsb3dlZF9tZXJjaGFudHMiLCAiYWxsb3dlZCI6IFt7Ii4uLiI6ICJhNVVNQWR4Q2tfTVJheXlWZFJocElBWjBaaGpWTEVxMWcyQld5cndLVXdnIn1dfV0sICJjbmYiOiB7Imp3ayI6IHsiY3J2IjogIlAtMjU2IiwgImt0eSI6ICJFQyIsICJ4IjogIlFwU3l4UFFIeTM4eGNreXZEcjU0Z1ozVDQyemo5aUx0VjRrb3liNVUyN2MiLCAieSI6ICIzN0hMZDdKSmlueGpKSW44SjdIaWpzc29lY0JsZmhkVy1nVUw3ZmVJOWx3In19LCAiaWF0IjogMTc3NzM0MjM1NywgImV4cCI6IDE3NzczNDU5NTd9XQ~
```


### SD-JWT do closed Checkout Mandate com disclosures

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
          "...": "7VLY-eKTFSShLoZRXY5jXcD2UHm1JvPmoANYRqqxy34"
        }
      ],
      "iat": 1777342376,
      "aud": "merchant",
      "nonce": "b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4",
      "sd_hash": "FzLoxbbtgQGYZxoSM2NJYJtkFTSsdfUBoVEQ12k7JN8",
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "FzLoxbbtgQGYZxoSM2NJYJtkFTSsdfUBoVEQ12k7JN8",
      "decoded": [
        "w-n1leFT6z8rHTNHwr5Wow",
        "checkout_jwt",
        {
          "header": {
            "alg": "ES256",
            "typ": "JWT"
          },
          "payload": {
            "order_id": "09414145-b7bi-432e-bf5c-ha0ba0bc4580",
            "merchant": {
              "id": "merchant_1",
              "name": "Demo Merchant",
              "website": "https://demo-merchant.example"
            },
            "line_items": [
              {
                "id": "line_1",
                "product": {
                  "id": "supershoe_limited_edition_gold_sneaker_womens_9_0",
                  "title": "SuperShoe Limited Edition Gold — Women's 9",
                  "price": 199.0,
                  "currency": "USD"
                },
                "quantity": 1
              }
            ],
            "total_price": 199.0,
            "currency": "USD",
            "shipping_policy": "Standard Shipping",
            "return_policy": "30-day returns"
          }
        }
      ]
    },
    {
      "digest": "7VLY-eKTFSShLoZRXY5jXcD2UHm1JvPmoANYRqqxy34",
      "decoded": [
        "szhpxKrgGJwyqMEN9WI5Sw",
        {
          "_sd": [
            "3A9UyZJofw2eMP-Lx2tYaNpCcuB8elnhwwLhZLwqFFM"
          ],
          "vct": "mandate.checkout.1",
          "checkout_hash": "NivWhuqfzcvZNapvIEJ2-3tsdQLkiuIcye2g46WVgX8"
        }
      ]
    }
  ]
}
```

#### Token codificado

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImtiK3NkLWp3dCJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIjdWTFktZUtURlNTaExvWlJYWTVqWGNEMlVIbTFKdlBtb0FOWVJxcXh5MzQifV0sICJpYXQiOiAxNzc3MzQyMzc2LCAiYXVkIjogIm1lcmNoYW50IiwgIm5vbmNlIjogImI5YzhkN2U2ZjVhNGIzYzJkMWUwZjlhOGI3YzZkNWU0IiwgInNkX2hhc2giOiAiRnpMb3hiYnRnUUdZWnhvU00yTkpZSnRrRlRTc2RmVUJvVkVRMTJrN0pOOCIsICJfc2RfYWxnIjogInNoYS0yNTYifQ.lSjkli6K3NbKlWOl1gJdWDwiyL88yJVyx32ZJHmvCXfRoItnchXw-MLUDEJv7o9lmTeipS42qNt7Z_oGSnRH1w~WyJzeGhweEtyZ0dKd3lxTUVNOVdJNVN3IiwgeyJfc2QiOiBbIjNBOVV5WkpvZncyZU1QLUx4MnRZYU5wQ2N1QjhlbG5od3dMaFpMd3FRRk0iXSwgInZjdCI6ICJtYW5kYXRlLmNoZWNrb3V0LjEiLCAiY2hlY2tvdXRfaGFzaCI6ICJOaXZXaHVxZnpjdlpOYXB2SUVKMi0zdHNkUUxraXVJY3llMmc0NldWZ1g4In1d~WyJ3LW4xbGVGVDZ6OHJIVE5Id3I1V293IiwgImNoZWNrb3V0X2p3dCIsICJleUpoYkdjaU9pQWlSVk15TlRZaUxDQWlkSGx3SWpvZ0lrcFhWQ0lzSUNKcmFXUWlPaUFpYldWeVkyaGhiblF0YTJWNUxURWlmUS5leUpwWkNJNklDSXdPVFF4TkRFME5TMWlOekJpTFRRNE0yRXRZamcxWXkxaFlUQm1ZVEJqTkRVNE1EQWlMQ0FpYldWeVkyaGhiblFpT2lCN0ltbGtJam9nSW0xbGNtTm9ZVzUwWHpFaUxDQWlibUZ0WlNJNklDSkVaVzF2SUUxbGNtTm9ZVzUwSWl3Z0luZGxZbk5wZEdVaU9pQWlhSFIwY0hNNkx5OWtaVzF2TFcxbGNtTm9ZVzUwTG1WNFlXMXdiR1VpZlN3Z0lteHBibVZmYVhSbGJYTWlPaUJiZXlKcFpDSTZJQ0pzYVY4d0lpd2dJbWwwWlcwaU9pQjdJbWxrSWpvZ0luTjFjR1Z5YzJodlpWOXNhVzFwZEdWa1gyVmthWFJwYjI1ZloyOXNaRjl6Ym1WaGEyVnlYM2R2YldWdWMxODVYekFpTENBaWRHbDBiR1VpT2lBaVUzVndaWEp6YUc5bElFeHBiV2wwWldRZ1JXUnBkR2x2YmlCSGIyeGtJRk51WldGclpYSWdWMjl0Wlc1eklEa2lMQ0FpY0hKcFkyVWlPaUF4T1Rrd01IMHNJQ0p4ZFdGdWRHbDBlU0k2SURFc0lDSjBiM1JoYkhNaU9pQmJleUowZVhCbElqb2dJbk4xWW5SdmRHRnNJaXdnSW1GdGIzVnVkQ0k2SURFNU9UQXdmU3dnZXlKMGVYQmxJam9nSW5SdmRHRnNJaXdnSW1GdGIzVnVkQ0k2SURFNU9UQXdmVjE5WFN3Z0luTjBZWFIxY3lJNklDSnBibU52YlhCc1pYUmxJaXdnSW1OMWNuSmxibU41SWpvZ0lsVlRSQ0lzSUNKMGIzUmhiSE1pT2lCYmV5SjBlWEJsSWpvZ0luTjFZblJ2ZEdGc0lpd2dJbUZ0YjNWdWRDSTZJREU1T1RBd2ZTd2dleUowZVhCbElqb2dJblJ2ZEdGc0lpd2dJbUZ0YjNWdWRDSTZJREU1T1RBd2ZWMHNJQ0pzYVc1cmN5STZJRnQ3SW5SNWNHVWlPaUFpY0hKcGRtRmplVjl3YjJ4cFkza2lMQ0FpZFhKc0lqb2dJbWgwZEhCek9pOHZhSFIwY0hNdkwyUmxiVzh0YldWeVkyaGhiblF1WlhoaGJYQnNaUzl3Y21sMllXTjVJbjBzSUhzaWRIbHdaU0k2SUNKMFpYSnRjMTl2Wmw5elpYSjJhV05sSWl3Z0luVnliQ0k2SUNKb2RIUndjem92TDJoMGRIQnpMeTlrWlcxdkxXMWxjbU5vWVc1MExtVjRZVzF3YkdVdmRHOXpJbjFkZlEuUC1WS3poeUp1bzktUlBpTjVheW5naDdmTFVLY09QQWVaejczU09Zd2Q1UDlZWG1HTE9yTFRXeGdYdkd5UVF0dERETTVELUc0czE5dnhfVTY1ZHJ1UmciXQ~
```

### Open Checkout Mandate encadeado com um closed Checkout Mandate após o processamento do Delegate SD-JWT.

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
          "...": "QtXTJtWqg999CmUWGjHFTWMkRPguDfeK3wGSaInd-dw"
        }
      ],
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "y3aocAD2rhYpJQOUMN016faDFGkTBGEDVl1R1TRHdbw",
      "decoded": [
        "4n3L_-3_Fm2GgyFAF8Ct_g",
        {
          "id": "supershoe_limited_edition_gold_sneaker_womens_9_0",
          "title": "SuperShoe Limited Edition Gold"
        }
      ]
    },
    {
      "digest": "a5UMAdxCk_MRayyVdRhpIAZ0ZhjVLEq1g2BWyruKUwg",
      "decoded": [
        "2zPL6vqLBg2WYAdbW9-1lQ",
        {
          "id": "merchant_1",
          "name": "Demo Merchant",
          "website": "https://demo-merchant.example"
        }
      ]
    },
    {
      "digest": "QtXTJtWqg999CmUWGjHFTWMkRPguDfeK3wGSaInd-dw",
      "decoded": [
        "laAoWKNRuGnwREjJWYJ7pg",
        {
          "vct": "mandate.checkout.open.1",
          "constraints": [
            {
              "type": "checkout.line_items",
              "items": [
                {
                  "id": "line_1",
                  "acceptable_items": [
                    {
                      "...": "y3aocAD2rhYpJQOUMN016faDFGkTBGEDVl1R1TRHdbw"
                    }
                  ],
                  "quantity": 1
                }
              ]
            },
            {
              "type": "checkout.allowed_merchants",
              "allowed": [
                {
                  "...": "a5UMAdxCk_MRayyVdRhpIAZ0ZhjVLEq1g2BWyruKUwg"
                }
              ]
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
          "...": "7VLY-eKTFSShLoZRXY5jXcD2UHm1JvPmoANYRqqxy34"
        }
      ],
      "iat": 1777342376,
      "aud": "merchant",
      "nonce": "b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4",
      "sd_hash": "FzLoxbbtgQGYZxoSM2NJYJtkFTSsdfUBoVEQ12k7JN8",
      "_sd_alg": "sha-256"
    }
  },
  "disclosures": [
    {
      "digest": "7VLY-eKTFSShLoZRXY5jXcD2UHm1JvPmoANYRqqxy34",
      "decoded": [
        "szhpxKrgGJwyqMEN9WI5Sw",
        {
          "_sd": [
            "3A9UyZJofw2eMP-Lx2tYaNpCcuB8elnhwwLhZLwqFFM"
          ],
          "vct": "mandate.checkout.1",
          "checkout_hash": "NivWhuqfzcvZNapvIEJ2-3tsdQLkiuIcye2g46WVgX8"
        }
      ]
    },
    {
      "digest": "FzLoxbbtgQGYZxoSM2NJYJtkFTSsdfUBoVEQ12k7JN8",
      "decoded": [
        "w-n1leFT6z8rHTNHwr5Wow",
        "checkout_jwt",
        {
          "header": {
            "alg": "ES256",
            "typ": "JWT"
          },
          "payload": {
            "order_id": "09414145-b7bi-432e-bf5c-ha0ba0bc4580",
            "merchant": {
              "id": "merchant_1",
              "name": "Demo Merchant",
              "website": "https://demo-merchant.example"
            },
            "line_items": [
              {
                "id": "line_1",
                "product": {
                  "id": "supershoe_limited_edition_gold_sneaker_womens_9_0",
                  "title": "SuperShoe Limited Edition Gold — Women's 9",
                  "price": 199.0,
                  "currency": "USD"
                },
                "quantity": 1
              }
            ],
            "total_price": 199.0,
            "currency": "USD",
            "shipping_policy": "Standard Shipping",
            "return_policy": "30-day returns"
          }
        }
      ]
    }
  ]
}
```

#### Token codificado

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgImtpZCI6ICJhZ2VudC1wcm92aWRlci1rZXktMSJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIlF0WFRKdFdxZzk5OUNtVVdHakhGVFdNa1JQZ3VEZmVLM3dHU2FJbmQtZHcifV0sICJfc2RfYWxnIjogInNoYS0yNTYifQ.HvCGk7ye_c0LN2-NFG13wfyu3LA--rckTPGm36ugO2aRvsded7ngw1py8W3JF7wBpoQnsKr17tNTF3zLeYcoWA~WyI0bjNMXy0zX0ZtMkdneUZBRjhDdF9nIiwgeyJpZCI6ICJzdXBlcnNob2VfbGltaXRlZF9lZGl0aW9uX2dvbGRfc25lYWtlcl93b21lbnNfOV8wIiwgInRpdGxlIjogIlN1cGVyU2hvZSBMaW1pdGVkIEVkaXRpb24gR29sZCJ9XQ~WyIyelBMNnZxTEJnMldZQWRiVzktMWxRIiwgeyJpZCI6ICJtZXJjaGFudF8xIiwgIm5hbWUiOiAiRGVtbyBNZXJjaGFudCIsICJ3ZWJzaXRlIjogImh0dHBzOi8vZGVtby1tZXJjaGFudC5leGFtcGxlIn1d~WyJsYUFvV0tOUnVHbndSRWpKV1lKN3BnIiwgeyJ2Y3QiOiAibWFuZGF0ZS5jaGVja291dC5vcGVuLjEiLCAiY29uc3RyYWludHMiOiBbeyJ0eXBlIjogImNoZWNrb3V0LmxpbmVfaXRlbXMiLCAiaXRlbXMiOiBbeyJpZCI6ICJsaW5lXzEiLCAiYWNjZXB0YWJsZV9pdGVtcyI6IFt7Ii4uLiI6ICJ5M2FvY0FEMnJoWXBKUU9VTU4wMTZmYURGR2tUQkdFRFZsMVIxVFJIZGJ3In1dLCAicXVhbnRpdHkiOiAxfV19LCB7InR5cGUiOiAiY2hlY2tvdXQuYWxsb3dlZF9tZXJjaGFudHMiLCAiYWxsb3dlZCI6IFt7Ii4uLiI6ICJhNVVNQWR4Q2tfTVJheXlWZFJocElBWjBaaGpWTEVxMWcyQld5cndLVXdnIn1dfV0sICJjbmYiOiB7Imp3ayI6IHsiY3J2IjogIlAtMjU2IiwgImt0eSI6ICJFQyIsICJ4IjogIlFwU3l4UFFIeTM4eGNreXZEcjU0Z1ozVDQyemo5aUx0VjRrb3liNVUyN2MiLCAieSI6ICIzN0hMZDdKSmlueGpKSW44SjdIaWpzc29lY0JsZmhkVy1nVUw3ZmVJOWx3In19LCAiaWF0IjogMTc3NzM0MjM1NywgImV4cCI6IDE3NzczNDU5NTd9XQ~~eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImtiK3NkLWp3dCJ9.eyJkZWxlZ2F0ZV9wYXlsb2FkIjogW3siLi4uIjogIjdWTFktZUtURlNTaExvWlJYWTVqWGNEMlVIbTFKdlBtb0FOWVJxcXh5MzQifV0sICJpYXQiOiAxNzc3MzQyMzc2LCAiYXVkIjogIm1lcmNoYW50IiwgIm5vbmNlIjogImI5YzhkN2U2ZjVhNGIzYzJkMWUwZjlhOGI3YzZkNWU0IiwgInNkX2hhc2giOiAiRnpMb3hiYnRnUUdZWnhvU00yTkpZSnRrRlRTc2RmVUJvVkVRMTJrN0pOOCIsICJfc2RfYWxnIjogInNoYS0yNTYifQ.lSjkli6K3NbKlWOl1gJdWDwiyL88yJVyx32ZJHmvCXfRoItnchXw-MLUDEJv7o9lmTeipS42qNt7Z_oGSnRH1w~WyJzeGhweEtyZ0dKd3lxTUVNOVdJNVN3IiwgeyJfc2QiOiBbIjNBOVV5WkpvZncyZU1QLUx4MnRZYU5wQ2N1QjhlbG5od3dMaFpMd3FRRk0iXSwgInZjdCI6ICJtYW5kYXRlLmNoZWNrb3V0LjEiLCAiY2hlY2tvdXRfaGFzaCI6ICJOaXZXaHVxZnpjdlpOYXB2SUVKMi0zdHNkUUxraXVJY3llMmc0NldWZ1g4In1d~WyJ3LW4xbGVGVDZ6OHJIVE5Id3I1V293IiwgImNoZWNrb3V0X2p3dCIsICJleUpoYkdjaU9pQWlSVk15TlRZaUxDQWlkSGx3SWpvZ0lrcFhWQ0lzSUNKcmFXUWlPaUFpYldWeVkyaGhiblF0YTJWNUxURWlmUS5leUpwWkNJNklDSXdPVFF4TkRFME5TMWlOekJpTFRRNE0yRXRZamcxWXkxaFlUQm1ZVEJqTkRVNE1EQWlMQ0FpYldWeVkyaGhiblFpT2lCN0ltbGtJam9nSW0xbGNtTm9ZVzUwWHpFaUxDQWlibUZ0WlNJNklDSkVaVzF2SUUxbGNtTm9ZVzUwSWl3Z0luZGxZbk5wZEdVaU9pQWlhSFIwY0hNNkx5OWtaVzF2TFcxbGNtTm9ZVzUwTG1WNFlXMXdiR1VpZlN3Z0lteHBibVZmYVhSbGJYTWlPaUJiZXlKcFpDSTZJQ0pzYVY4d0lpd2dJbWwwWlcwaU9pQjdJbWxrSWpvZ0luTjFjR1Z5YzJodlpWOXNhVzFwZEdWa1gyVmthWFJwYjI1ZloyOXNaRjl6Ym1WaGEyVnlYM2R2YldWdWMxODVYekFpTENBaWRHbDBiR1VpT2lBaVUzVndaWEp6YUc5bElFeHBiV2wwWldRZ1JXUnBkR2x2YmlCSGIyeGtJRk51WldGclpYSWdWMjl0Wlc1eklEa2lMQ0FpY0hKcFkyVWlPaUF4T1Rrd01IMHNJQ0p4ZFdGdWRHbDBlU0k2SURFc0lDSjBiM1JoYkhNaU9pQmJleUowZVhCbElqb2dJbk4xWW5SdmRHRnNJaXdnSW1GdGIzVnVkQ0k2SURFNU9UQXdmU3dnZXlKMGVYQmxJam9nSW5SdmRHRnNJaXdnSW1GdGIzVnVkQ0k2SURFNU9UQXdmVjE5WFN3Z0luTjBZWFIxY3lJNklDSnBibU52YlhCc1pYUmxJaXdnSW1OMWNuSmxibU41SWpvZ0lsVlRSQ0lzSUNKMGIzUmhiSE1pT2lCYmV5SjBlWEJsSWpvZ0luTjFZblJ2ZEdGc0lpd2dJbUZ0YjNWdWRDSTZJREU1T1RBd2ZTd2dleUowZVhCbElqb2dJblJ2ZEdGc0lpd2dJbUZ0YjNWdWRDSTZJREU1T1RBd2ZWMHNJQ0pzYVc1cmN5STZJRnQ3SW5SNWNHVWlPaUFpY0hKcGRtRmplVjl3YjJ4cFkza2lMQ0FpZFhKc0lqb2dJbWgwZEhCek9pOHZhSFIwY0hNdkwyUmxiVzh0YldWeVkyaGhiblF1WlhoaGJYQnNaUzl3Y21sMllXTjVJbjBzSUhzaWRIbHdaU0k2SUNKMFpYSnRjMTl2Wmw5elpYSjJhV05sSWl3Z0luVnliQ0k2SUNKb2RIUndjem92TDJoMGRIQnpMeTlrWlcxdkxXMWxjbU5vWVc1MExtVjRZVzF3YkdVdmRHOXpJbjFkZlEuUC1WS3poeUp1bzktUlBpTjVheW5naDdmTFVLY09QQWVaejczU09Zd2Q1UDlZWG1HTE9yTFRXeGdYdkd5UVF0dERETTVELUc0czE5dnhfVTY1ZHJ1UmciXQ~
```

## Tipos comuns

### Item

{{ schema_fields('open_checkout_mandate', 'ap2', show_sd=True,
pointer='#/$defs/item') }}

### LineItemRequirements

{{ schema_fields('open_checkout_mandate', 'ap2', show_sd=True,
pointer='#/$defs/line_item_requirements') }}

### Merchant

{{ schema_fields('types/merchant', 'ap2', show_sd=True) }}
