# Código

Todo o código-fonte do AP2 fica aqui, separado por artefato.

## `sdk/` — o SDK do AP2

O artefato principal deste repositório. A implementação em Python fica em
[`sdk/python/ap2/`](sdk/python/ap2/) e é o pacote exposto pelo
[`pyproject.toml`](../pyproject.toml) da raiz (instalado como `import ap2`).

Conteúdo:

- `sdk/python/ap2/models/` — modelos Pydantic para carrinhos, mandates,
  receipts e solicitações de pagamento.
- `sdk/python/ap2/schemas/` — JSON Schemas canônicos e o gerador usado para
  emitir os modelos Python em `sdk/python/ap2/sdk/generated/`.
- `sdk/python/ap2/sdk/` — o SDK de runtime: wrappers de mandate, verificação
  de cadeia, utilitários de SD-JWT, constraints, metadados de disclosure.
- `sdk/python/ap2/tests/` — testes unitários do SDK.

SDKs em outras linguagens (Go, JS, …) ficariam ao lado deste, dentro de `sdk/`.

## `samples/` — implementações de referência

Cenários de ponta a ponta que demonstram o protocolo:

- [`samples/python/`](samples/python/) — papéis em Python (merchant,
  credentials provider, shopping agent, payment processor) e cenários.
- [`samples/go/`](samples/go/) — servidores de referência e cenários em Go.
- [`samples/android/`](samples/android/) — assistente de compras para Android
  e o cenário de credenciais de pagamento digitais.
- [`samples/certs/`](samples/certs/) — CA e certificados folha de teste
  usados pelos exemplos na verificação de confiança de SD-JWT.

## `web-client/` — interface de demonstração

Um app Vite + React + TypeScript que exercita o protocolo A2A com os agentes de
exemplo.
