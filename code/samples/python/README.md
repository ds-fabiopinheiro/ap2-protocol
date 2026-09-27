# Exemplos em Python do Agent Payments Protocol (AP2)

Implementações de referência em Python dos papéis do AP2 (merchant,
credentials provider, payment processor, shopping agent) e cenários de ponta a
ponta que os integram.

Todos os caminhos abaixo são relativos à raiz do repositório.

## Estrutura

- [`scenarios/`](./scenarios) — fluxos de ponta a ponta executáveis. Cada
  cenário tem um `run.sh` (ou `run_*.sh`) que sobe todos os agentes/servidores
  de que precisa.
- [`src/roles/`](./src/roles) — as implementações de cada papel usadas por
  esses cenários.
- [`src/common/`](./src/common) — utilitários compartilhados (cliente A2A,
  construtores de mensagens, inicialização de servidor etc.).

Para exemplos em outras linguagens, veja [`../go/`](../go) e
[`../android/`](../android). Os certificados de teste usados pelos exemplos
ficam em [`../certs/`](../certs).

## Pré-requisitos

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)
- Uma chave de API do Google do [Google AI Studio](https://aistudio.google.com/apikey),
  ou ADC do Vertex AI (`GOOGLE_GENAI_USE_VERTEXAI=true`).

## Configuração

Crie um arquivo `.env` na raiz do repositório com pelo menos a sua chave de API:

```
GOOGLE_API_KEY=<your_api_key>
```

Alguns cenários (por exemplo, `shopping_agent_v2`) leem variáveis adicionais de
um `.env` local dentro do diretório do papel — veja o README do cenário quando
for o caso. Por exemplo:

```
GOOGLE_API_KEY=<your_api_key>
AGENT_MODEL=gemini-3.1-flash-lite-preview
```

## Como executar um cenário

Escolha um cenário e execute o script dele a partir da raiz do repositório.
Cada script cria/atualiza o ambiente virtual do `uv` e inicia todos os agentes
de que precisa.

Human-present (shopping agent interativo, no navegador):

```bash
./code/samples/python/scenarios/a2a/human-present/cards/run.sh
./code/samples/python/scenarios/a2a/human-present/cards/run.sh --payment-method x402
```

Human-not-present (fluxos automatizados / recorrentes):

```bash
./code/samples/python/scenarios/a2a/human-not-present/cards/run.sh
./code/samples/python/scenarios/a2a/human-not-present/x402/run.sh
```

Veja o README dentro do diretório de cada cenário para o passo a passo do
fluxo e as interações esperadas.
