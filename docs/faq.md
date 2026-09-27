# Perguntas frequentes

1. O que posso fazer com este protocolo hoje?

    - Criamos agentes de exemplo com base na biblioteca Python principal do AP2
      que demonstram uma experiência de compra completa. Inicie os agentes e
      experimente comprar seus produtos favoritos\! Estes exemplos simulam
      provedores de serviços de pagamento reais, então você pode explorá-los sem
      dependências. Em especial, observe os Mandates (autorizações assinadas)
      enquanto os agentes trabalham. Publicaremos mais exemplos e SDKs em breve,
      e queremos conhecer suas ideias\! Você pode usar os exemplos de código para
      criar sua própria implementação de um pagamento entre vários agentes de IA
      ou estender o protocolo para mostrar novos tipos de cenário de pagamento
      _(por exemplo, um pagamento feito com outro método de pagamento ou com
      outra forma de autenticação)_.

1. Posso criar meu próprio agente para algum destes papéis, usando um deles
   como modelo?

    - Sim, você pode criar seu próprio agente para qualquer um dos
      [papéis](ap2/implementation_considerations.md). Comece a construir com o
      [ADK](https://google.github.io/adk-docs/) e o
      [Agent Builder](https://cloud.google.com/products/agent-builder) do
      Google Cloud, ou com qualquer outra plataforma de agentes que preferir.

1. Posso criar meu próprio agente para participar deste protocolo?

    - Sim, você pode criar um agente para qualquer um dos
      [papéis](ap2/implementation_considerations.md) definidos. Qualquer agente,
      em qualquer framework (como LangGraph, AG2 ou CrewAI) ou em qualquer
      runtime, pode implementar o AP2.

1. Posso testar sem fazer um pagamento de verdade?

    - Você pode configurar o protocolo nos seus ambientes internos, onde talvez
      já existam formas de acionar métodos de pagamento fictícios que não
      movimentam dinheiro real.

1. Existe um servidor MCP ou um SDK pronto para o "meu framework preferido"?

    - Estamos trabalhando em um SDK e em um servidor MCP neste momento, em
      colaboração com provedores de serviços de pagamento. Volte em breve.

1. Isso funciona com o padrão x402 para pagamentos com cripto?

    - Projetamos o AP2 para ser um protocolo independente do meio de pagamento,
      de modo que o comércio por agentes possa acontecer com segurança em todos
      os tipos de sistema de pagamento. Ele fornece uma base segura e auditável,
      seja quando o agente usa um cartão de crédito, seja quando faz transações
      com stablecoins. Esse desenho flexível permite estender seus princípios
      a novos ecossistemas, com um padrão de confiança consistente em todos eles.

        Como primeiro passo, veja
        [google-agentic-commerce/a2a-x402](https://github.com/google-agentic-
commerce/a2a-x402/),
        uma implementação do A2A em conjunto com o padrão x402.
        Com o tempo, vamos alinhá-la ao AP2 para facilitar a composição de
        soluções que incluam todos os métodos de pagamento, inclusive
        stablecoins.

1. O que são verifiable credentials?

    - São objetos de dados padronizados e criptograficamente seguros (como o
      Checkout Mandate e o Payment Mandate) que servem como blocos de
      construção de uma transação: assinados criptograficamente, com
      adulteração detectável e não contestáveis.

1. Como o protocolo garante controle e privacidade ao usuário?

    - O protocolo foi projetado para que o usuário seja sempre a autoridade
      final e tenha controle detalhado sobre as atividades dos seus agentes. Ele
      protege informações sensíveis do usuário, como prompts da conversa e dados
      pessoais de pagamento, impedindo que os shopping agents acessem dados
      sensíveis de PCI ou PII por meio de criptografia do payload e de selective
      disclosure (divulgação seletiva), para garantir a minimização de dados.

1. Como o AP2 trata a responsabilização das transações?

    - Um dos objetivos principais é fornecer evidências que ajudem as redes de
      pagamento a estabelecer princípios de responsabilização e de
      responsabilidade. Em uma disputa, o árbitro da rede (por exemplo, a
      bandeira do cartão) pode usar o Checkout Mandate assinado pelo usuário e
      comparar os detalhes do que foi combinado entre o agente e o consumidor
      com os detalhes da disputa, para ajudar a determinar a responsabilização
      pela transação.

1. O que impede um agente de "alucinar" e fazer uma compra incorreta?

    - O princípio da intenção verificável, e não da ação inferida, trata esse
      risco. As transações devem se apoiar em uma prova determinística e
      irrefutável da intenção de todas as partes, como o Checkout Mandate
      assinado pelo usuário, em vez de depender só da interpretação das saídas
      probabilísticas e ambíguas de um modelo de linguagem.

1. Por que o suporte a cripto e Web3 foi incluído desde o início?

    - Aceitar uma ampla variedade de tipos de pagamento, inclusive métodos de
      pagamento digitais, prepara o protocolo para o futuro. A colaboração com
      parceiros como Coinbase, Ethereum Foundation e Metamask valida a
      flexibilidade do AP2 e aproxima a economia tradicional da economia Web3,
      permitindo novos casos de uso, como micropagamentos.

1. Como posso participar?

    - O AP2 é um projeto de código aberto criado pelo Google, assim como o
      protocolo A2A. Contribuições são bem-vindas no GitHub na forma de
      discussões, bugs, solicitações de funcionalidade e PRs. A colaboração já
      está acontecendo, com novos exemplos, integrações e SDKs em
      desenvolvimento – o GitHub é a melhor forma de se comunicar com a equipe
      do AP2.

1. Qual é a diferença entre UCP e AP2? E qual a relação com o recurso de
   checkout por agente de vocês?

    - AP2: o Agent Payments Protocol (AP2) foi projetado para oferecer uma
      linguagem comum para que agentes façam transações com segurança e
      responsabilização. Enquanto o Universal Commerce Protocol orquestra o
      ciclo de vida da compra como um todo, o AP2 é a camada de pagamento
      especializada, responsável por autorizar e assinar as transações. O AP2
      se torna essencial no fluxo quando, em um futuro próximo, as transações
      passarem a ser de fato feitas por agentes e os usuários delegarem compras
      aos seus agentes de IA. Esse desenho modular promove confiança entre
      compradores, merchants e provedores, mantendo a flexibilidade.
      Os merchants poderão integrar o AP2 como extensão do Universal Commerce
      Protocol para transações conduzidas por agentes de IA.

    - Checkout por agente: nosso recurso de checkout por agente compra itens em
      seu nome diretamente no site de uma loja, conforme suas instruções. O
      Universal Commerce Protocol é diferente porque permite a compra nativa
      no AI Mode e no Gemini. Quando compram de forma nativa no AI Mode e no
      Gemini, os usuários são conectados diretamente ao merchant, o que
      habilita recursos adicionais, como sinais importantes de pós-compra (por
      exemplo, atualizações de status do pedido). Benefícios que estarão
      disponíveis em breve incluem o uso de pontos de fidelidade e a compra a
      partir de um carrinho anterior.

1. Como sei quando usar o AP2?

    - Se você é um merchant que quer exibir produtos e permitir que os usuários
    concluam o checkout diretamente nas superfícies de IA do Google, como o AI
    Mode e o Gemini, use o Universal Commerce Protocol. Você pode complementar
    o protocolo com a extensão AP2 se pretende criar cenários de compra
    autônoma, em que agentes de IA fazem compras na ausência do usuário.

    - Fora das superfícies de descoberta do Google, se você quer habilitar um
    fluxo de pagamento entre dois agentes de IA ou adicionar verifiable
    credentials aos fluxos de pagamento entre sua superfície de descoberta e um
    agente de IA, você pode continuar usando o AP2.

1. Quais são os próximos passos do AP2?

    - O trabalho na especificação principal continuará na [FIDO](https://blog.google/products-and-platforms/platforms/google-pay/agent-payments-protocol-fido-alliance/), para que ela continue sendo um protocolo aberto e interoperável para todos os pagamentos feitos por agentes.
    - Os exemplos de código e o SDK continuarão sendo aprimorados e seguirão como uma implementação atualizada da especificação do AP2.
