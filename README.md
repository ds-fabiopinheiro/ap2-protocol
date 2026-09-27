# Agent Payments Protocol (AP2)

[![Apache License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/google-agentic-commerce/AP2)

<!-- markdownlint-disable MD041 -->
<p align="center">
  <img src="docs/assets/ap2_graphic.png" alt="Agent Payments Protocol Graphic">
</p>

Este repositório contém exemplos de código e demonstrações do Agent Payments Protocol.

## Vídeo de introdução ao AP2

[![Vídeo de introdução ao A2A](https://img.youtube.com/vi/jSHj0z9Gi24/hqdefault.jpg)](https://youtu.be/jSHj0z9Gi24?si=JyzMu2wZCMpVuxvv)

### AP2 no The Agent Factory - setembro de 2025

[![The Agent Factory (September 2025) - Episode 8: Agent payments, can you do my shopping?](https://img.youtube.com/vi/T1MtWnEYXM0/hqdefault.jpg)](https://youtu.be/T1MtWnEYXM0?si=QkJWnAiav0JAP9F6)

## Sobre os exemplos

Estes exemplos usam o [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) e o Gemini 3.1 Flash Lite Preview.

O Agent Payments Protocol não exige o uso de nenhum dos dois. Eles foram usados
nos exemplos, mas você pode usar as ferramentas que preferir para construir
seus agentes.

## Estrutura do repositório

A estrutura de nível superior é:

- [**`docs/`**](docs/) — especificação, fluxos, FAQ e fontes do MkDocs.
- [**`code/`**](code/) — todo o código-fonte, organizado por artefato:
    - [**`code/sdk/`**](code/sdk/) — o SDK do AP2 (o Python fica em
      [`code/sdk/python/ap2/`](code/sdk/python/ap2/)).
    - [**`code/samples/`**](code/samples/) — implementações de referência e
      cenários.
    - [**`code/web-client/`**](code/web-client/) — o web client de demonstração
      (Vite + React).

O diretório **`samples`** contém uma coleção de cenários selecionados para
demonstrar os principais componentes do Agent Payments Protocol.

Os cenários ficam em:

- [**`code/samples/python/scenarios`**](code/samples/python/scenarios) — Python.
- [**`code/samples/go/scenarios`**](code/samples/go/scenarios) — Go.
- [**`code/samples/android/scenarios`**](code/samples/android/scenarios) — Android.

Cada cenário contém:

- um arquivo `README.md` que descreve o cenário e as instruções para executá-lo.
- um script `run.sh` que simplifica a execução local do cenário.

A demonstração inclui vários agentes e servidores; a maior parte do código-fonte
fica em [**`code/samples/python/src`**](code/samples/python/src/).
Os cenários que usam um app Android como assistente de compras têm o código-fonte
em [**`code/samples/android`**](code/samples/android/); os papéis em Go ficam em
[**`code/samples/go`**](code/samples/go/).

Para a referência da API do SDK, veja
[**`code/sdk/python/ap2/sdk/README.md`**](code/sdk/python/ap2/sdk/README.md).

## Início rápido

### Pré-requisitos

- Python 3.11 ou superior
- Gerenciador de pacotes [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

### Configuração

A autenticação pode ser feita com uma Google API Key ou com o Vertex AI.

Nos dois métodos, você pode definir as credenciais necessárias como variáveis de ambiente no shell ou colocá-las em um arquivo `.env` na raiz do projeto.

#### Opção 1: Google API Key (recomendada para desenvolvimento)

1. Obtenha uma Google API Key no [Google AI Studio](http://aistudio.google.com/apikey).
2. Defina a variável de ambiente `GOOGLE_API_KEY`.

    - **Como variável de ambiente:**

        ```sh
        export GOOGLE_API_KEY='your_key'
        ```

    - **Em um arquivo `.env`:**

        ```sh
        GOOGLE_API_KEY='your_key'
        ```

#### Opção 2: [Vertex AI](https://cloud.google.com/vertex-ai) (recomendada para produção)

1. **Configure o ambiente para usar o Vertex AI.**
    - **Como variáveis de ambiente:**

        ```sh
        export GOOGLE_GENAI_USE_VERTEXAI=true
        export GOOGLE_CLOUD_PROJECT='your-project-id'
        export GOOGLE_CLOUD_LOCATION='global' # ou a região de sua preferência
        ```

    - **Em um arquivo `.env`:**

        ```sh
        GOOGLE_GENAI_USE_VERTEXAI=true
        GOOGLE_CLOUD_PROJECT='your-project-id'
        GOOGLE_CLOUD_LOCATION='global'
        ```

2. **Autentique a aplicação.**
    - **Usando a [CLI `gcloud`](https://cloud.google.com/sdk/docs/install):**

        ```sh
        gcloud auth application-default login
        ```

    - **Usando uma Service Account:**

        ```sh
        export GOOGLE_APPLICATION_CREDENTIALS='/path/to/your/service-account-key.json'
        ```

### Como executar um cenário

Para executar um cenário específico, siga as instruções do `README.md` dele. Em
geral, o procedimento é este:

1. Vá até a raiz do repositório.

    ```sh
    cd AP2
    ```

1. Execute o script de execução para instalar as dependências e iniciar os
   agentes. O caminho exato depende do cenário — por exemplo, o fluxo de
   pagamento com cartão human-present:

    ```sh
    bash code/samples/python/scenarios/a2a/human-present/cards/run.sh
    ```

    Os outros cenários ficam ao lado dele, em
    `code/samples/python/scenarios/`, `code/samples/go/scenarios/` e
    `code/samples/android/scenarios/` (veja o `README.md` de cada cenário
    para o comando exato).

1. Abra a URL do Shopping Agent e comece a interagir.

### Instalação do pacote de tipos do AP2

Os objetos principais do protocolo são definidos em
[`code/sdk/python/ap2/`](code/sdk/python/ap2/) — modelos Pydantic em
[`models/`](code/sdk/python/ap2/models/) e
[`sdk/generated/`](code/sdk/python/ap2/sdk/generated/), JSON schemas canônicos
em [`schemas/`](code/sdk/python/ap2/schemas/). Um pacote no PyPI será publicado
posteriormente. Até lá, você pode instalar o pacote diretamente com este
comando:

```sh
uv pip install git+https://github.com/google-agentic-commerce/AP2.git@main
```
