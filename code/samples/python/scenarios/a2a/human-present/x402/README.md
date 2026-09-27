# Exemplo do Agent Payments Protocol: compras human-present com x402

Este exemplo mostra a extensão ap2-extension do A2A (protocolo Agent2Agent) em
uma transação human-present (com o usuário presente) que usa, como meio de
pagamento, meios compatíveis com x402.

**Observação:** a extensão x402 compatível com AP2 será lançada em breve. A
extensão x402 atual será ampliada para garantir a criação de todos os mandates
principais descritos no AP2. Veja o repositório atual da extensão x402 para A2A:
[repositório da extensão x402 para A2A](https://github.com/google-agentic-commerce/a2a-x402/).

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

* **Shopping Agent:** o orquestrador principal, que trata os pedidos de compra
    do usuário e delega tarefas a agentes especializados.
* **Merchant Agent:** um agente que responde às consultas de produtos do
    shopping agent.
* **Merchant Payment Processor Agent:** um agente que recebe pagamentos em
    nome do merchant.
* **Credentials Provider Agent:** o credentials provider é o detentor das
    credenciais de pagamento do usuário. Por isso, ele tem duas funções
    principais:
    * Fornece ao shopping agent a lista de meios de pagamento disponíveis na
        carteira do usuário.
    * Intermedeia o pagamento entre o shopping agent e o processador de
        pagamentos do merchant.

## Principais funcionalidades

### 1. Compra com x402

* O Merchant Agent anuncia suporte a compras com x402 no seu agent card e no
    CartMandate, quando as compras terminam.
* O meio de pagamento preferido na carteira do usuário será um meio de
    pagamento compatível com x402.

## Como executar o exemplo

### Configuração

Obtenha uma chave de API do Google no
[Google AI Studio](https://aistudio.google.com/apikey). Depois, declare a
variável GOOGLE_API_KEY de uma das duas formas.

* Opção 1: declare-a como variável de ambiente: `export
    GOOGLE_API_KEY=your_key`
* Opção 2: coloque-a em um arquivo .env na raiz do repositório. `echo
    "GOOGLE_API_KEY=your_key" > .env`

### Execução

Execute o comando abaixo para rodar todas as etapas em um único terminal:

```sh
code/samples/python/scenarios/a2a/human-present/cards/run.sh --payment-method x402
```

Ou execute cada servidor em um terminal próprio (confirme que `PAYMENT_METHOD=x402` está definido em todos os processos):

1. Inicie o Merchant Agent:

    ```sh
    export PAYMENT_METHOD=x402
    uv run --package ap2-samples python -m roles.merchant_agent
    ```

2. Inicie o Credentials Provider:

    ```sh
    export PAYMENT_METHOD=x402
    uv run --package ap2-samples python -m roles.credentials_provider_agent
    ```

3. Inicie o Merchant Payment Processor Agent:

    ```sh
    export PAYMENT_METHOD=x402
    uv run --package ap2-samples python -m roles.merchant_payment_processor_agent
    ```

4. Inicie o Shopping Agent:

    ```sh
    export PAYMENT_METHOD=x402
    uv run --package ap2-samples adk web code/samples/python/src/roles
    ```

Abra um navegador e acesse a interface do shopping agent em [http://0.0.0.0:8000](http://0.0.0.0:8000).
A partir daí você pode interagir com o Shopping Agent.

### Como interagir com o Shopping Agent

Esta seção descreve uma interação típica com o exemplo.

1. **Abrir a interface do Agent Development Kit**: abra um navegador no seu
    computador e acesse 0.0.0.0:8000/dev-ui. Selecione `shopping_agent` na lista
    `Select an agent`, no canto superior esquerdo.
1. **Pedido inicial**: no terminal do Shopping Agent, você será convidado a
    iniciar uma conversa. Você pode digitar algo como: "I want to buy a coffee
    maker."
1. **Busca de produtos**: o Shopping Agent delega a tarefa ao Merchant Agent,
    que encontra produtos correspondentes à sua intenção e apresenta opções
    contidas em CartMandates.
1. **Criação do carrinho**: o Merchant Agent cria um ou mais `CartMandate`s e
    os compartilha com o Shopping Agent. Cada CartMandate é assinado pelo
    Merchant, o que garante que a oferta ao usuário está correta.
1. **Seleção do produto** O Shopping Agent apresenta ao usuário o conjunto de
    produtos para escolha.
1. **Vincular o Credential Provider**: o Shopping Agent pede que você vincule o
    seu Credential Provider preferido para acessar os meios de pagamento
    disponíveis.
1. **Seleção do meio de pagamento**: depois que você seleciona um carrinho, o
    Shopping Agent mostra uma lista de meios de pagamento disponíveis vinda do
    Credentials Provider Agent. Você seleciona um meio de pagamento.
1. **Criação do PaymentMandate**: o Shopping Agent reúne as informações do
    carrinho e da transação em um PaymentMandate e pede que você assine o
    mandate. Em seguida, inicia o pagamento usando o PaymentMandate.
1. **Compra concluída**: o pagamento é processado (o desafio de OTP é dispensado na demonstração com x402) e você recebe uma mensagem de confirmação e um recibo digital.
