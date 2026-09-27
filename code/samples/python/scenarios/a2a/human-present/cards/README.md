# Exemplo do Agent Payments Protocol: compras human-present com cartão

Este exemplo mostra a extensão ap2-extension do A2A (protocolo Agent2Agent) em
uma transação human-present (com o usuário presente) que usa um cartão como meio
de pagamento.

## Cenário

Fluxos human-present são todos os fluxos de comércio em que o usuário está
presente para confirmar os detalhes do que está sendo comprado e qual meio de
pagamento será usado. Como o usuário atesta os detalhes da compra, todas as
partes têm alta confiança na transação.

O IntentMandate continua sendo usado para compartilhar as informações adequadas
com os Merchant Agents. O objetivo é manter a consistência entre os fluxos
human-present e human-not-present.

Todas as compras human-present terão um PaymentMandate assinado pelo usuário que
autoriza a compra.

## Principais atores

Este exemplo é composto por:

*   **Shopping Agent:** o orquestrador principal, que trata os pedidos de compra
    do usuário e delega tarefas a agentes especializados.
*   **Merchant Agent:** um agente que responde às consultas de produtos do
    shopping agent.
*   **Merchant Payment Processor Agent:** um agente que recebe pagamentos em
    nome do merchant.
*   **Credentials Provider Agent:** o credentials provider é o detentor das
    credenciais de pagamento do usuário. Por isso, ele tem duas funções
    principais:
    *   Fornece ao shopping agent a lista de meios de pagamento disponíveis na
        carteira do usuário.
    *   Intermedeia o pagamento entre o shopping agent e o processador de
        pagamentos do merchant.

## Principais funcionalidades

**1. Compra com cartão usando DPAN**

*   O merchant agent anuncia suporte a compras com cartão no seu agent card e
    no CartMandate, quando as compras terminam.
*   O meio de pagamento preferido na carteira do usuário será um cartão
    tokenizado (DPAN).

**2. Desafio de OTP**

*   O merchant payment processor agent solicita ao usuário um desafio de OTP
    (senha de uso único) para concluir o pagamento.

## Como executar o exemplo

### Configuração

Obtenha uma chave de API do Google no
[Google AI Studio](https://aistudio.google.com/apikey). Depois, declare a
variável GOOGLE_API_KEY de uma das duas formas.

*   Opção 1: declare-a como variável de ambiente: `export
    GOOGLE_API_KEY=your_key`
*   Opção 2: coloque-a em um arquivo .env na raiz do repositório. `echo
    "GOOGLE_API_KEY=your_key" > .env`

### Execução

Execute o comando abaixo para rodar todas as etapas em um único terminal:

```sh
bash code/samples/python/scenarios/a2a/human-present/cards/run.sh
```

Ou execute cada servidor em um terminal próprio:

1.  Inicie o Merchant Agent:

    ```sh
    uv run --package ap2-samples python -m roles.merchant_agent
    ```

2.  Inicie o Credentials Provider:

    ```sh
    uv run --package ap2-samples python -m roles.credentials_provider_agent
    ```

3.  Inicie o Merchant Payment Processor Agent:

    ```sh
    uv run --package ap2-samples python -m roles.merchant_payment_processor_agent
    ```

4.  Inicie o Shopping Agent:

    ```sh
    uv run --package ap2-samples adk web code/samples/python/src/roles
    ```

Abra um navegador e acesse a interface do shopping agent em http://0.0.0.0:8000.
A partir daí você pode interagir com o Shopping Agent.

### Como interagir com o Shopping Agent

Esta seção descreve uma interação típica com o exemplo.

1.  **Abrir a interface do Agent Development Kit**: abra um navegador no seu
    computador e acesse 0.0.0.0:8000/dev-ui. Selecione `shopping_agent` na lista
    `Select an agent`, no canto superior esquerdo.
1.  **Pedido inicial**: no terminal do Shopping Agent, você será convidado a
    iniciar uma conversa. Você pode digitar algo como: "I want to buy a coffee
    maker."
1.  **Busca de produtos**: o Shopping Agent delega a tarefa ao Merchant Agent,
    que encontra produtos correspondentes à sua intenção e apresenta opções
    contidas em CartMandates.
1.  **Criação do carrinho**: o Merchant Agent cria um ou mais `CartMandate`s e
    os compartilha com o Shopping Agent. Cada CartMandate é assinado pelo
    Merchant, o que garante que a oferta ao usuário está correta.
1.  **Seleção do produto** O Shopping Agent apresenta ao usuário o conjunto de
    produtos para escolha.
1.  **Vincular o Credential Provider**: o Shopping Agent pede que você vincule o
    seu Credential Provider preferido para acessar os meios de pagamento
    disponíveis.
1.  **Seleção do meio de pagamento**: depois que você seleciona um carrinho, o
    Shopping Agent mostra uma lista de meios de pagamento disponíveis vinda do
    Credentials Provider Agent. Você seleciona um meio de pagamento.
1.  **Criação do PaymentMandate**: o Shopping Agent reúne as informações do
    carrinho e da transação em um PaymentMandate e pede que você assine o
    mandate. Em seguida, inicia o pagamento usando o PaymentMandate.
1.  **Desafio de OTP**: o Merchant Payment Processor solicita um OTP, e você
    precisa informar um OTP simulado ao agente. Use `123`
1.  **Compra concluída**: depois que o OTP é informado, o pagamento é
    processado e você recebe uma mensagem de confirmação e um recibo digital.

## Usos avançados dos exemplos

### Como ativar respostas detalhadas do Shopping Agent

Se você quiser entender o que os agentes fazem internamente ou inspecionar os
objetos de mandate que eles criam e compartilham, peça ao Shopping Agent para
rodar em **modo verbose**.

O modo verbose instrui o Shopping Agent, e os agentes para os quais ele delega
tarefas, a dar explicações detalhadas do processo, incluindo:

*   Uma descrição das etapas atuais e das próximas.
*   A representação JSON de todos os payloads de dados (como `IntentMandates`,
    `CartMandates` ou `PaymentMandates`) criados, enviados ou recebidos.

#### Como ativar o modo verbose

Para ativar esse modo, inclua a palavra-chave verbose no seu prompt inicial ao
Shopping Agent. Exemplo de prompt:

*"I'm looking to buy a new pair of shoes. Could you be verbose as we do this,
explaining what you're doing, and display all data payloads?"*

> **💡 DICA: dê instruções detalhadas**
>
> Embora a palavra **verbose** normalmente seja suficiente, instruções mais
> detalhadas no prompt tendem a gerar explicações mais completas e úteis do
> agente.

> **💡 DICA: se o JSON não aparecer...**
>
> Se o agente estiver em modo verbose mas não exibir o JSON do mandate,
> normalmente basta um prompt curto de acompanhamento. Diga: **"Remember we're
> in verbose mode, please display the JSON."** Depois desse lembrete, o agente
> costuma exibir todos os payloads de dados com mais regularidade.

### Como ver a comunicação entre os agentes

Para ajudar engenheiros a visualizar a comunicação exata entre os servidores dos
agentes, um arquivo de log detalhado é criado automaticamente quando os
servidores iniciam.

Por padrão, esse arquivo de log se chama `watch.log` e fica no diretório
`.logs`.

#### Conteúdo do log

O watch log é um rastro completo que inclui três categorias principais de
dados:

| Categoria                  | Detalhes incluídos                                   |
| :------------------------- | :--------------------------------------------------- |
| **Dados HTTP brutos**      | O **método HTTP** (ex.: `POST`) e a **URL** de cada  |
:                            : requisição, o **corpo JSON da requisição** e o       :
:                            : **corpo JSON da resposta**.                          :
| **Dados de mensagens A2A** | As **instruções da requisição** extraídas do         |
:                            : `TextPart` da mensagem Agent-to-Agent (A2A) e os     :
:                            : dados encontrados nos `DataParts` da mensagem.       :
| **Dados do protocolo AP2** | Os **objetos Mandate** (`IntentMandate`,             |
:                            : `CartMandate`, `PaymentMandate`) identificados nos   :
:                            : `DataParts` de uma mensagem.                         :
