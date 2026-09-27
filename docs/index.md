---
hide:
    - toc
---

<!-- markdownlint-disable MD041 -->
<div style="text-align: center;">
  <div class="centered-logo-text-group">
    <img src="assets/ap2-logo-black.svg" alt="Agent Payments Protocol Logo" width="100">
    <h1>Agent Payments Protocol (AP2)</h1>
  </div>
</div>

## O que é o AP2?

**O Agent Payments Protocol (AP2) é um protocolo aberto para a economia de
agentes que está surgindo.** Ele foi projetado para permitir comércio por agentes
seguro, confiável e interoperável para desenvolvedores, merchants e o setor de
pagamentos. O protocolo está disponível como extensão do
[protocolo Agent2Agent (A2A)](https://a2a-protocol.org/), de código aberto, e do
[Universal Commerce Protocol](https://ucp.dev/documentation/ucp-and-ap2/), e há
outras integrações em andamento.


<!-- prettier-ignore-start -->
!!! abstract ""

    Construa agentes com
    **[![ADK Logo](https://google.github.io/adk-docs/assets/agent-development-kit.png){class="twemoji lg middle"} ADK](https://google.github.io/adk-docs/)**
    _(ou qualquer framework)_, equipe-os com
    **[![MCP Logo](https://modelcontextprotocol.io/mcp.png){class="twemoji lg middle"} MCP](https://modelcontextprotocol.io)**
    _(ou qualquer ferramenta)_, faça-os colaborar via
    **[![A2A Logo](https://a2a-protocol.org/latest/assets/a2a-logo-black.svg){class="twemoji sm middle"} A2A](https://a2a-protocol.org)** e use o
    **![AP2 Logo](./assets/ap2-logo-black.svg){class="twemoji sm middle"} AP2** para proteger pagamentos feitos por agentes de IA generativa.
<!-- prettier-ignore-end -->

<div class="grid cards" markdown>

- :material-play-circle:{ .lg .middle } **Vídeo** de introdução em menos de 7 min

    ---

      <iframe width="560" height="315" src="https://www.youtube.com/embed/jSHj0z9Gi24?si=jDx8luqpw35nbDKy" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- :material-file-document-outline:{ .lg .middle } **Leia a documentação**

    ---

    [:octicons-arrow-right-24: Lançamento do AP2 v0.2 e doação à FIDO Alliance](https://blog.google/products-and-platforms/platforms/google-pay/agent-payments-protocol-fido-alliance/)

    [:octicons-arrow-right-24: FIDO Alliance desenvolverá padrões para interações confiáveis com agentes de IA](https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/)

    [:octicons-arrow-right-24: Anúncio do Agent Payments Protocol (16/09/2025)](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)

    &nbsp;

    **Veja a definição técnica detalhada do protocolo AP2**

    [:octicons-arrow-right-24: Especificação do Agent Payments Protocol](ap2/specification.md)

    [:octicons-arrow-right-24: Guia de integração entre AP2 e UCP](https://ucp.dev/documentation/ucp-and-ap2/)

</div>

---

## Por que um protocolo de pagamentos para agentes é necessário

Os sistemas de pagamento atuais partem do princípio de que uma pessoa clica
diretamente em "comprar" em um site confiável. Quando um agente autônomo inicia
um pagamento, essa premissa deixa de valer, e surgem perguntas que os sistemas
atuais não conseguem responder:

- **Autorização:** como verificar que o usuário deu ao agente autoridade
    específica para uma determinada compra?
- **Autenticidade:** como o merchant pode ter certeza de que a solicitação do
    agente reflete com precisão a real intenção do usuário, sem erros nem
    "alucinações" da IA?
- **Responsabilização:** se ocorrer uma transação fraudulenta ou incorreta,
    quem é responsável — o usuário, o desenvolvedor do agente, o merchant, o
    issuer, o PSP ou a camada de orquestração?

Essa ambiguidade gera um problema de confiança que pode limitar bastante a
adoção. Sem um protocolo comum, há o risco de um ecossistema fragmentado de
soluções de pagamento proprietárias, confuso para os usuários, caro para os
merchants e difícil de administrar para as instituições financeiras. O AP2
busca criar uma linguagem comum para que qualquer agente compatível faça
transações com segurança com qualquer merchant compatível, em qualquer país.

---

## Princípios e objetivos

O Agent Payments Protocol se baseia em princípios definidos para criar um
ecossistema seguro e justo:

- **Abertura e interoperabilidade:** como extensão aberta e não proprietária do
    A2A e do MCP, o AP2 favorece um ambiente competitivo para inovação, amplo
    alcance de merchants e liberdade de escolha para o usuário.
- **Controle e privacidade do usuário:** o usuário deve estar sempre no
    controle. O protocolo tem a privacidade como base e usa uma arquitetura
    baseada em papéis para proteger dados de pagamento sensíveis e informações
    pessoais.
- **Intenção verificável, e não ação inferida:** a confiança nos pagamentos se
    apoia em uma prova determinística e irrefutável da intenção do usuário, o
    que trata diretamente o risco de erro ou alucinação do agente.
- **Responsabilização clara das transações:** o AP2 fornece uma trilha de
    auditoria criptográfica e irrefutável para cada transação, o que ajuda na
    resolução de disputas e dá confiança a todos os participantes.
- **Global e preparado para o futuro:** projetado como base global, a versão
    inicial aceita métodos de pagamento "pull" comuns, como cartões de crédito
    e débito. O roadmap inclui carteiras digitais, pagamentos "push", como
    transferências bancárias em tempo real (por exemplo, UPI e PIX), e moedas
    digitais, considerando que muitos países não têm sistemas bancários em
    tempo real.

---

## Conceito principal: Verifiable Digital Credentials (VDCs)

O Agent Payments Protocol estabelece confiança no sistema por meio de
**verifiable digital credentials (VDCs)** (credenciais digitais verificáveis).
VDCs são objetos digitais assinados criptograficamente, nos quais qualquer
adulteração é detectável, e servem de base para compor uma transação. Há dois
tipos principais de Mandates (autorizações assinadas), cada um com dois estágios:

- **Checkout Mandate**: registra a referência aos itens específicos e aos
  detalhes da compra negociados entre o agente e o merchant, e é
  **compartilhado com o merchant**.
    - **Open**: registra as constraints (restrições) e os objetivos do usuário
      para a transação antes que um carrinho específico seja finalizado para
      execução autônoma.
    - **Closed**: registra a autorização do usuário (ou do agente) para um
      checkout específico e finalizado.
- **Payment Mandate**: autoriza um pagamento com um instrumento de pagamento
  específico e é **compartilhado com o Credential Provider, as redes e o
  Merchant Payment Processor**.
    - **Open**: registra as constraints do usuário sobre o pagamento (por
      exemplo, orçamento, instrumentos permitidos) para execução autônoma.
    - **Closed**: registra a autorização de um valor de transação específico
      vinculado a um checkout finalizado.

Essas VDCs operam dentro de uma arquitetura definida baseada em papéis e são
encadeadas para fornecer uma trilha de auditoria completa e verificável, tanto
em transações human-present (com a pessoa presente) quanto human-not-present
(sem a pessoa presente).

Veja mais nos [Fluxos](ap2/flows.md) de exemplo.

## Veja na prática

<div class="grid cards" markdown>

- **Cards (human-not-present)**

    ---

    Exemplo de uma transação autônoma em que o agente age sem a presença da pessoa, com pagamento por cartão tradicional.

    [:octicons-arrow-right-24: Ir para o exemplo](https://github.com/google-agentic-commerce/AP2/tree/main/code/samples/python/scenarios/a2a/human-not-present/cards/)

- **x402 (human-not-present)**

    ---

    Exemplo de uma transação autônoma em que o agente age sem a presença da pessoa, com pagamento pelo protocolo x402.

    [:octicons-arrow-right-24: Ir para o exemplo](https://github.com/google-agentic-commerce/AP2/tree/main/code/samples/python/scenarios/a2a/human-not-present/x402/)

- **Digital Payment Credentials (Android)**

    ---

    Exemplo do uso de credenciais digitais de pagamento em um dispositivo Android.

    [:octicons-arrow-right-24: Ir para o exemplo](https://github.com/google-agentic-commerce/AP2/tree/main/code/samples/android/scenarios/digital-payment-credentials/)

- **Cards (human-present)**

    ---

    Exemplo de uma transação human-present com pagamento por cartão tradicional.

    [:octicons-arrow-right-24: Ir para o exemplo](https://github.com/google-agentic-commerce/AP2/tree/main/code/samples/python/scenarios/a2a/human-present/cards/)

</div>

---

## Como começar e contribuir

O Agent Payments Protocol fornece um mecanismo para pagamentos seguros e faz
parte de um conjunto maior de iniciativas para viabilizar o comércio feito por
agentes. Buscamos ativamente seu feedback e suas contribuições.

Nosso repositório público no GitHub hospeda a versão mais recente da especificação, da documentação e do SDK do AP2. A padronização da especificação continuará nos grupos de trabalho Agentic Authentication Technical e Payments Technical da FIDO.

Para começar agora, você pode:

- Baixar e executar nossos **exemplos de código**.
- **Experimentar o protocolo** e os diferentes papéis de agente.
- Enviar seu feedback e **código** para o repositório público.

[Acesse o repositório no GitHub](https://github.com/google-agentic-commerce/AP2)
