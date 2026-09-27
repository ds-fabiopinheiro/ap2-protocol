# Sample em Go: pagamento com cartão human-present (A2A)

Este cenário mostra um fluxo de pagamento com cartão human-present (usuário
presente durante a compra) usando agentes em Go.

**O que está incluído:**

- Merchant Agent - catálogo de produtos e gestão do carrinho
- Credentials Provider - credenciais de pagamento e carteira
- Payment Processor - processamento de pagamentos e desafios OTP

**Observação:** este sample trata dos agentes em Go. Use o Shopping Agent
em Python para interagir com esses agentes.

## Agentes implementados

- **Merchant Agent** (`http://localhost:8001/a2a/merchant_agent`)
    - Atende consultas ao catálogo de produtos
    - Cria e gerencia cart mandates
    - Expõe a skill `search_catalog` para intenções de compra
    - Suporta as extensões AP2 e Sample Card Network

- **Credentials Provider Agent**
  (`http://localhost:8002/a2a/credentials_provider`)
    - Gerencia as credenciais de pagamento e a carteira do usuário
    - Fornece detalhes dos meios de pagamento
    - Fornece dados do cartão tokenizado (DPAN)
    - Trata a autorização do pagamento

- **Merchant Payment Processor Agent**
  (`http://localhost:8003/a2a/merchant_payment_processor_agent`)
    - Processa pagamentos em nome dos merchants
    - Implementa o mecanismo de desafio OTP
    - Trata a autorização e a liquidação do pagamento

## O que este sample mostra

1. **Recursos do protocolo AP2**
    - Ciclo de vida completo do mandate (Intent → Cart → Payment)
    - Suporte a pagamento com cartão usando tokens DPAN
    - Fluxos de desafio OTP
    - Mecanismo de extensões (AP2 + extensões de meio de pagamento)

2. **Padrões de serviços de backend**
    - Serviços modulares, implantáveis de forma independente
    - Separação clara de responsabilidades
    - Pontos fortes do Go para serviços de backend (concorrência, segurança
      de tipos, desempenho)

3. **Protocolo independente de linguagem**
    - Agentes de backend em Go funcionam com o Shopping Agent em Python
    - Mostra interoperabilidade real entre linguagens
    - Mostra que o protocolo independe da implementação

## Como executar o sample

### Pré-requisitos

- Go 1.21 ou superior
- Make
- Chave de API do Google obtida no [Google AI Studio](https://aistudio.google.com/apikey)

### Início rápido

1. **Configure sua chave de API:**

   ```sh
   export GOOGLE_API_KEY=your_key
   ```

   Ou crie um arquivo `.env` em `code/samples/go/`:

   ```sh
   echo "GOOGLE_API_KEY=your_key" > code/samples/go/.env
   ```

2. **Execute todos os agentes `go`:**

   ```sh
   # A partir da raiz do repositório
   bash code/samples/go/scenarios/a2a/human-present/cards/run.sh
   ```

   Isso inicia os três agentes de backend:

   - Merchant Agent na porta 8001
   - Credentials Provider na porta 8002
   - Payment Processor na porta 8003

### Compilação e execução manual

```sh
cd code/samples/go

# Instala as dependências
go mod download

# Compila todos os agentes
make build

# Executa cada agente (em terminais separados)
./bin/merchant_agent
./bin/credentials_provider_agent
./bin/merchant_payment_processor_agent
```

## Fluxo de compra completo

Para mostrar o fluxo de compra de ponta a ponta com os agentes em Go, é
possível usar o Shopping Agent em Python.

### Shopping Agent em Python + agentes `go`

Isso mostra **interoperabilidade entre linguagens**.

1. **Inicie os agentes de backend em Go** (veja [Início rápido](#início-rápido))

2. **Inicie o Shopping Agent em Python em outro terminal:**

   ```sh
   # A partir da raiz do repositório
   uv run --package ap2-samples adk web code/samples/python/src/roles
   ```

   O Shopping Agent em Python já vem configurado para se conectar aos backends
   em Go em `code/samples/python/src/roles/shopping_agent/remote_agents.py`:

   ```python
   merchant_agent_client = PaymentRemoteA2aClient(
       name="merchant_agent",
       base_url="http://localhost:8001/a2a/merchant_agent",  # Go agent
       required_extensions={EXTENSION_URI},
   )

   credentials_provider_client = PaymentRemoteA2aClient(
       name="credentials_provider",
       base_url="http://localhost:8002/a2a/credentials_provider",  # Go agent
       required_extensions={EXTENSION_URI},
   )
   ```

3. **Abra o navegador** em `http://localhost:8000` e faça compras.

   Você terá:

   - **Shopping Agent**: Python (com a interface web do ADK)
   - **Agentes de backend**: Go (merchant, credentials, payment processor)

   Para testar:
   - Selecione "Shopping Agent" no menu suspenso no canto superior esquerdo
   - Pergunte: "Hello, I'd like to buy a pair of red running shoes."
   - Siga a conversa para concluir o fluxo de compra

### Teste direto da API

Você pode testar os agentes em Go diretamente com requisições HTTP:

**Obter informações do merchant agent:**

```sh
curl -X POST http://localhost:8001/a2a/merchant_agent \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "agent.info",
    "params": {},
    "id": 1
  }'
```

**Buscar produtos:**

```sh
curl -X POST http://localhost:8001/a2a/merchant_agent \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "agent.invoke",
    "params": {
      "skill": "search_catalog",
      "input": {
        "shopping_intent": "{\"product_type\": \"coffee maker\"}"
      }
    },
    "id": 2
  }'
```

**Obter meios de pagamento:**

```sh
curl -X POST http://localhost:8002/a2a/credentials_provider \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "agent.invoke",
    "params": {
      "skill": "get_payment_method"
    },
    "id": 3
  }'
```

## Estrutura do projeto

```text
code/samples/go/
├── cmd/                                  # Agent entry points
│   ├── merchant_agent/main.go
│   ├── credentials_provider_agent/main.go
│   └── merchant_payment_processor_agent/main.go
├── pkg/
│   ├── ap2/types/                       # AP2 protocol types
│   │   ├── mandate.go                   # Mandate structures
│   │   ├── payment_request.go
│   │   └── contact_address.go
│   ├── common/                          # Shared infrastructure
│   │   ├── base_executor.go            # Base agent execution
│   │   ├── message_builder.go          # A2A message construction
│   │   ├── server.go                   # HTTP/JSON-RPC server
│   │   └── function_resolver.go        # Tool/skill handling
│   └── roles/                           # Agent implementations
│       ├── merchant_agent/
│       │   ├── agent.json              # Capabilities & skills
│       │   ├── executor.go             # Business logic
│       │   ├── tools.go                # Agent tools
│       │   └── storage.go              # Product catalog
│       ├── credentials_provider_agent/
│       │   ├── agent.json
│       │   └── executor.go
│       └── merchant_payment_processor_agent/
│           ├── agent.json
│           └── executor.go
└── scenarios/a2a/human-present/cards/
    ├── README.md                        # This file
    └── run.sh                           # Start all agents
```

## Desenvolvimento

### Execução dos testes

```sh
cd code/samples/go
make test
```

### Formatação do código

```sh
make fmt
```

### Como adicionar um novo agente de backend

1. Crie o ponto de entrada em `cmd/your_agent/main.go`
2. Implemente o executor em `pkg/roles/your_agent/executor.go`
3. Defina o `agent.json` com capabilities e skills
4. Adicione o alvo de build ao `Makefile`
5. Atualize o `run.sh` para iniciar o novo agente

## Como parar os agentes

Se você usou o `run.sh`, pressione `Ctrl+C` para parar todos os agentes.

Se executou manualmente, pare cada processo individualmente.

## Próximos passos

- **Executar o fluxo completo**: use o Shopping Agent em Python com estes
  backends em Go
- **Explorar o código**: veja como o protocolo AP2 é implementado em Go
- **Construir o seu**: use estes agentes como referência para os seus agentes AP2

## Recursos

- [Documentação do protocolo AP2](../../../../README.md)
- [Sample em Python (com Shopping Agent)](../../../../python/scenarios/a2a/human-present/cards/README.md)
- [Guia da implementação em Go](../../README.md)

## Licença

Copyright 2025 Google LLC. Licenciado sob a Apache License, Version 2.0.
