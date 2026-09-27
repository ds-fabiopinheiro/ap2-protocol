# Exemplo do Agent Payments Protocol: compras human-not-present com x402

Este exemplo mostra uma transação **human-not-present** (sem o usuário presente
no momento da compra) que usa meios de pagamento compatíveis com **x402**.

## Cenário

Fluxos human-not-present são todos os fluxos de comércio em que o usuário **não
está presente** para confirmar os detalhes do que está sendo comprado no
momento exato da transação. Em vez disso, o usuário autorizou antes os detalhes
da transação e o meio de pagamento (por exemplo, ao definir uma intenção
específica ou aceitar uma condição de compra, como uma queda de preço).

Neste cenário, o fluxo é disparado por um evento simulado de "queda de preço"
ou "disponibilidade do item" enviado pelo merchant. Quando o preço cai para um
valor aceitável para o agente (com base na intenção do usuário), o Shopping
Agent (agente de compras que atua em nome do usuário) conclui a compra de forma
autônoma, usando as credenciais e os mandates autorizados previamente, sem
pedir confirmação ao usuário em tempo real.

## Principais atores

Este exemplo é composto por:

- **Shopping Agent (v2):** o orquestrador principal, que trata os pedidos de
  compra do usuário e age de forma autônoma quando uma condição de disparo é
  atendida.
- **Merchant Agent (MCP):** um agente que responde a consultas de produtos e
  anuncia suporte a compras com x402.
- **x402 Merchant Payment Processor Agent (MCP):** um agente que recebe
  pagamentos em nome do merchant.
- **x402 Credentials Provider Agent (MCP):** o detentor das credenciais de
  pagamento do usuário, que intermedeia o pagamento entre o shopping agent e o
  processador de pagamentos do merchant.

## Principais funcionalidades

**1. Compra autônoma a partir de um disparo**

- O fluxo começa por um disparo externo (uma queda de preço ou disponibilidade
  de item simulada), e não por um comando direto do usuário no momento da
  compra.
- O agente avalia a condição e segue com a compra se ela corresponder à
  intenção do usuário.

**2. Integração de compras com x402**

- O Merchant Agent anuncia suporte a compras com x402 no seu agent card e no
  CartMandate.
- O fluxo usa meios de pagamento compatíveis com x402 e normalmente dispensa
  etapas manuais, como desafios de OTP, o que o torna adequado para interações
  autônomas de agentes.

## Como executar o exemplo

### Configuração

Obtenha uma chave de API do Google no
[Google AI Studio](https://aistudio.google.com/apikey). Depois, declare a
variável GOOGLE_API_KEY de uma das duas formas:

- **Opção 1:** declare-a como variável de ambiente:
  `export GOOGLE_API_KEY=your_key`
- **Opção 2:** coloque-a em um arquivo `.env` na raiz do repositório:
  `echo "GOOGLE_API_KEY=your_key" > .env`

### Execução

Execute o comando abaixo para iniciar todos os serviços (Merchant Trigger, x402
PSP Trigger, Shopping Agent e Web Client) em um único terminal:

```sh
bash code/samples/python/scenarios/a2a/human-not-present/x402/run.sh
```

Para ativar a simulação de transmissão na blockchain (se o cenário oferecer
suporte), passe a flag:

```sh
bash code/samples/python/scenarios/a2a/human-not-present/x402/run.sh \
  --enable_broadcast_on_chain
```

O script inicia os serviços nas seguintes portas:

- Agent: `8080`
- Merchant Trigger: `8081`
- x402 PSP Trigger: `8084`
- Web Client: `5173`

O script abre o web client no navegador automaticamente. Se isso não
acontecer, abra `http://localhost:5173` manualmente.

### Como disparar o fluxo

Para simular a condição de disparo (por exemplo, uma queda de preço), abra outro
terminal e execute o comando abaixo (substitua `<item_id>` e `<price>` por
valores de teste adequados):

```sh
curl -X POST \
  "http://localhost:8081/trigger-price-drop?item_id=<item_id>&price=<price>&stock=10"
```

Acompanhe o web client para ver a compra autônoma acontecendo.
