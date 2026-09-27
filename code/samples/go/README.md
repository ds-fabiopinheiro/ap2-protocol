# Samples em Go do Agent Payments Protocol AP2

Este diretório contém samples em Go que mostram como construir agentes
AP2.

## Cenários disponíveis

No momento, há um cenário disponível:

- **[Pagamento com cartão human-present](./scenarios/a2a/human-present/cards/README.md)**
    - Fluxo completo de pagamento com cartão, com agentes em Go e Shopping
      Agent em Python

Consulte o [README do cenário](./scenarios/a2a/human-present/cards/README.md)
para instruções detalhadas de configuração e uso.

## Por que Go para agentes de backend

Go pode ser especialmente adequado para construir serviços de backend do AP2:

- **Segurança de tipos**: validação das estruturas do protocolo em tempo de compilação
- **Desempenho**: respostas rápidas e baixo uso de recursos
- **Concorrência**: tratamento eficiente de requisições concorrentes
- **Implantação**: binário único, sem dependências de runtime

## Estrutura do projeto

```text
code/samples/go/
├── cmd/                               # Agent entry points
├── pkg/
│   ├── ap2/types/                    # AP2 protocol types
│   ├── common/                       # Shared infrastructure
│   └── roles/                        # Agent implementations
└── scenarios/                        # Runnable examples
    └── a2a/
        └── human-present/
            └── cards/                # Card payment scenario
```

## Desenvolvimento

```sh
# Executa os testes
make test

# Formata o código
make fmt

# Compila todos os agentes
make build
```

## Licença

Copyright 2025 Google LLC. Licenciado sob a Apache License, Version 2.0.
