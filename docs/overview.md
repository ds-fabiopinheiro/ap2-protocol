# Resumo executivo

Agentes de IA vão redefinir o cenário do comércio digital, com a promessa de
conveniência, personalização e eficiência sem precedentes. Essa mudança, porém,
expõe um desafio fundamental: a infraestrutura de pagamentos existente não foi
projetada para um futuro em que agentes autônomos, não humanos, atuam em nome de
um usuário ou fazem transações entre si. Os protocolos de pagamento atuais,
construídos sobre a premissa de interação direta iniciada por um humano em
interfaces confiáveis, não têm mecanismos para validar com segurança a
autenticidade de um agente e sua autoridade para transacionar. Isso gera
ambiguidade sobre a responsabilidade pelas transações e ameaça a adoção do
comércio agêntico.

Sem um protocolo comum e confiável, o setor corre o risco de um ecossistema
fragmentado e inseguro, formado por soluções proprietárias e isoladas que
aumentam a complexidade para os lojistas, criam atrito para os usuários e
impedem que as instituições financeiras avaliem o risco de forma uniforme. Para
cobrir essa lacuna, este documento propõe um protocolo aberto e interoperável
para pagamentos feitos por agentes. O protocolo, projetado como extensão dos
protocolos emergentes agent-to-agent (A2A), model-context protocols (MCP) e
Universal Commerce Protocol (UCP), estabelece uma estrutura segura e confiável
para o comércio conduzido por IA.

## A nova fronteira do comércio: por que pagamentos por agentes exigem um
protocolo fundamental

### 1.1 O crescimento do comércio por agentes

A evolução da interação digital está entrando em uma nova fase, que vai além da
manipulação direta de interfaces e passa para a execução de tarefas por conversa
e por delegação. Agentes de IA estão se tornando rapidamente atores principais,
capazes de entender pedidos complexos dos usuários e executar tarefas de várias
etapas de forma autônoma. No comércio, isso se traduz em uma mudança de
paradigma em que agentes vão cuidar de tudo, desde compras rotineiras e gestão
de assinaturas até pesquisa complexa de produtos, negociação de preços e
montagem dinâmica de pedidos com vários fornecedores. Essa nova era do comércio
por agentes promete gerar grande valor, oferecendo aos usuários uma experiência
de compra hiperpersonalizada
e sem atrito e dando aos lojistas novos canais inteligentes para
alcançar e atender clientes.

### 1.2 A lacuna fundamental: crise de confiança e de responsabilidade

Apesar do potencial, o crescimento do comércio por agentes expõe uma
vulnerabilidade crítica na infraestrutura atual de pagamentos digitais. Os
protocolos de pagamento de hoje são projetados em torno do princípio de um
usuário humano interagindo diretamente com uma interface confiável, como o site
de um lojista ou o aplicativo de um provedor de pagamentos. Autenticação,
autorização e responsabilidade dependem dessa participação humana direta.

Agentes autônomos quebram essa premissa. Quando um agente inicia um pagamento,
surgem questões fundamentais que os sistemas atuais não estão preparados para
responder:

* Autorização e auditabilidade: que prova verificável demonstra que o usuário
concedeu ao agente a autoridade específica para fazer esta compra em particular?
* Autenticidade da intenção: como um lojista ou processador de pagamentos pode
ter certeza de que o pedido do agente reflete com precisão a intenção real do
usuário humano?
* Erro do agente e "alucinação": como o sistema se protege contra erros do
agente, como interpretar mal o pedido do usuário ou "alucinar" detalhes de
produtos, o que poderia levar a compras incorretas?
* Responsabilização: no caso de uma transação fraudulenta ou incorreta, quem é
responsável? O usuário que delegou a tarefa? O desenvolvedor do shopping
agent? O lojista que aceitou o pedido? A rede de pagamento que a
processou? Ou a camada de PSP/orquestração?

Essa ambiguidade cria uma crise de confiança. Sem uma estrutura robusta para
validar a autoridade do agente e atribuir responsabilidade com clareza, as
instituições financeiras podem hesitar em aprovar transações iniciadas por
agentes, os lojistas ficarão expostos a níveis inaceitáveis de risco de fraude e
os usuários relutarão em delegar autoridade financeira a agentes.

### 1.3 O risco de um ecossistema fragmentado

Na ausência de um protocolo adotado universalmente, o setor inevitavelmente
caminhará para uma colcha de retalhos de soluções proprietárias e fechadas.
Grandes varejistas poderiam desenvolver integrações sob medida para seus agentes
específicos, e provedores de pagamento poderiam criar ecossistemas isolados que
não interoperam. Essa fragmentação teria consequências negativas graves:

* Para os usuários: uma experiência confusa e inconsistente, em que o agente
preferido pode funcionar apenas com um conjunto limitado de lojistas ou meios de
pagamento.
* Para os lojistas: altos custos de desenvolvimento e manutenção para suportar
várias integrações de pagamento por agentes fora de padrão, o que cria uma
barreira de entrada significativa para pequenas e médias empresas.
* Para o ecossistema de pagamentos: incapacidade de coletar sinais comuns em
todas as transações de agentes para mitigar fraudes de forma consistente, o que
leva a custos maiores e a taxas de aprovação de transações mais baixas.

Um protocolo aberto e interoperável é o caminho mais viável. Ele cria uma
linguagem comum para todos os participantes. Ele permite compartilhar dados
adicionais sobre a transação de uma forma que antes não era possível e garante
que qualquer agente compatível possa transacionar com segurança com qualquer
lojista compatível, favorecendo um mercado competitivo e inovador.

## Seção 2: Princípios orientadores para uma economia de agentes confiável

O desenho deste protocolo proposto se baseia em um conjunto de princípios
centrais, que têm o objetivo de construir um ecossistema sustentável, seguro e
equitativo para todos os participantes. Esses princípios são a base conceitual
da arquitetura técnica descrita a seguir.

### 2.1 Abertura e interoperabilidade

Este protocolo é proposto como uma extensão aberta e não proprietária dos
protocolos agent-to-agent (A2A), model-context protocol (MCP) e Universal
Commerce Protocol (UCP), atuais e futuros. O objetivo é
oferecer uma camada de pagamentos comum e interoperável que possa ser adotada
por qualquer participante do ecossistema. Essa abordagem favorece um ambiente
competitivo em que desenvolvedores podem inovar nas capacidades dos agentes,
lojistas podem alcançar o maior público possível e usuários podem escolher a
combinação de agentes e serviços que melhor atende às suas necessidades.

### 2.2 Controle do usuário e privacidade desde a concepção

O usuário deve ser sempre a autoridade final. O protocolo foi projetado para
garantir que os usuários tenham controle granular e visibilidade transparente
sobre as atividades de seus agentes.

A privacidade é um princípio central do desenho. O protocolo foi projetado para
proteger informações sensíveis do usuário, incluindo o conteúdo dos prompts de
conversa, os itens que ele compra e os dados de pagamento. Por meio de Selective
Disclosure (divulgação seletiva), os agentes envolvidos no processo de compra
ficam impedidos de acessar dados sensíveis da indústria de cartões de pagamento
(PCI), que são tratados exclusivamente pelas entidades especializadas e pelos
elementos seguros da infraestrutura de pagamento. Esse foco em privacidade e
minimização de dados também garante que cada entidade veja apenas os dados
estritamente necessários para exercer seu papel.

### 2.3 Intenção verificável, não ação inferida

A confiança em um sistema de agentes de IA não pode se basear apenas na
interpretação das saídas ambíguas e probabilísticas de um modelo de linguagem.
As transações precisam estar ancoradas em uma prova de intenção determinística e
irrefutável de todas as partes. Esse princípio trata diretamente do risco de
"alucinação" e de interpretação incorreta pelo agente.

### 2.4 Responsabilização clara pelas transações

Para que o ecossistema de pagamentos adote o comércio por agentes, não pode
haver ambiguidade quanto à responsabilização pelas transações. Um objetivo
principal deste protocolo é fornecer evidências que ajudem as redes de pagamento
a estabelecer princípios de responsabilização e de responsabilidade. Essa
clareza é requisito mínimo para obter a confiança e a participação de lojistas,
emissores e redes de pagamento.

## Seção 3: Visão geral da arquitetura: um ecossistema baseado em papéis para
transações seguras

Para atingir seus objetivos de segurança, interoperabilidade e responsabilização
clara, o protocolo proposto define uma arquitetura baseada em papéis. Cada ator
do ecossistema tem um conjunto distinto e bem definido de responsabilidades, o
que garante uma separação de atribuições que aumenta a segurança e simplifica a
integração.

O ecossistema de pagamentos por agentes é formado pelos seguintes papéis
principais:

* **Shopping Agent (SA):** o Shopping Agent (agente de compras) é o agente
principal, que faz a descoberta de produtos, monta o checkout e executa a
compra.
* **Credential Provider (CP):** o Credential Provider (provedor de credenciais)
é a origem das credenciais de pagamento da compra. Ele é responsável por
verificar se este agente está autorizado a acessar esta credencial de pagamento
e por limitar o escopo da credencial de pagamento de forma adequada.
* **Merchant (M)**: o Merchant (lojista) é a origem do checkout. Ele é
responsável pelo catálogo e pelo atendimento dos pedidos.
* **Merchant Payment Processor (MPP)**: o papel Merchant Payment Processor
(processador de pagamentos do lojista) é responsável por processar os pagamentos
das compras. Ele é responsável por verificar se a credencial de pagamento foi
autorizada a pagar este checkout.
* **Trusted Surface (TS):** o papel Trusted Surface (interface confiável) é uma
interface de usuário considerada confiável para obter o consentimento informado
do usuário para uma intenção antes de criar um Mandate (autorização assinada)
pelo usuário.
* **Network e Issuer**: o provedor da rede de pagamento e o emissor das
credenciais de pagamento para o usuário humano. O Credential Provider pode
precisar interagir com a rede para emitir tokens específicos para transações de
agentes de IA, e o Merchant/PSP pode enviar essas transações para autorização
dos emissores por meio das redes.

Alguns exemplos não normativos de como os papéis podem ser combinados: 

* O provedor do Shopping Agent pode também oferecer uma Trusted Surface não
agêntica dentro do seu aplicativo.
* O Shopping Agent pode também oferecer seu próprio Credential Provider.  
* O Merchant pode oferecer seu próprio Merchant Payment Processor  
* O Merchant pode ser um Credential Provider. 

## Seção 4: Principais jornadas do usuário

### 4.1 Transação human-present

O humano delega a um agente de IA uma tarefa que exige um pagamento (por
exemplo, uma compra) e está disponível quando o pagamento precisa ser
autorizado. Uma forma típica (mas não a única) de isso acontecer é a seguinte:

* Configuração: o usuário pode configurar uma conexão entre seu Shopping Agent
preferido e qualquer um dos Credential Providers suportados. Isso pode exigir
que o usuário se autentique em uma interface do Credential Provider.
* Descoberta e negociação: o usuário passa uma tarefa de compra para o agente de
IA escolhido (*que pode acionar um Shopping Agent especializado para concluir a
tarefa*). O Shopping Agent interage com um ou mais Merchants para montar um
carrinho que atenda ao pedido do usuário. Isso pode incluir a possibilidade de o
lojista fornecer informações de fidelidade, ofertas, venda cruzada e venda
adicional (*por meio da integração entre o Shopping Agent e o Merchant*), que o
Shopping Agent deve apresentar ao usuário .
* Merchant valida o carrinho: um SKU ou conjunto de SKUs é autorizado pelo
usuário para compra. O Shopping Agent comunica isso ao Merchant para iniciar a
criação do pedido. O Merchant precisa assinar o carrinho que cria para um
usuário, sinalizando que vai atender esse carrinho.
* Fornecer meios de pagamento: o Shopping Agent pode fornecer o contexto do
pagamento ao Credential Provider e solicitar um meio de pagamento aplicável
(compartilhado como referência ou de forma criptografada), junto com qualquer
informação de fidelidade/desconto que possa ser relevante para a escolha do meio
de pagamento (*por exemplo, pontos do cartão que podem ser resgatados na
transação*).
* Exibir o carrinho: o Shopping Agent apresenta o carrinho final e o meio de
pagamento aplicável ao usuário em uma trusted surface, e o usuário pode
aprová-lo por meio de um processo de autenticação.
* Assinar e pagar: a aprovação assinada do usuário precisa criar um “Checkout
Mandate” (autorização do usuário para um checkout) assinado criptograficamente.
Esse mandate contém os bens exatos que estão sendo comprados e a confirmação de
compra do usuário. Ele é compartilhado com o Merchant para que este possa
usá-lo como evidência em caso de disputa. Separadamente, o Payment Mandate
(autorização do usuário para o pagamento) pode ser compartilhado com a rede e o
emissor para autorização da transação.
* Execução do pagamento: o Payment Mandate precisa ser enviado ao Credential
Provider e ao Merchant para concluir a transação. Isso pode acontecer de várias
formas. Por exemplo,
  * o Shopping Agent (SA) pode pedir ao Credential Provider que conclua um
  pagamento com o Merchant OU
  * o SA pode enviar um pedido ao lojista, acionando um fluxo de autorização de
  pagamento em que o lojista/PSP solicita o meio de pagamento ao Credential
  Provider.
* Enviar a transação ao emissor: o Merchant ou PSP encaminha a transação ao
emissor ou à rede em que o meio de pagamento opera. O pacote da transação pode
receber sinais de presença de agente de IA, garantindo que a rede/emissor tenha
visibilidade sobre transações agênticas.
* Desafio: qualquer parte (emissor, Credential Provider, lojista etc.) pode
decidir desafiar a transação por mecanismos existentes, como o 3DS2. Esse
desafio precisa ser apresentado ao usuário pela Trusted Surface (*um exemplo
seria um 3DS hospedado*) e pode exigir um redirecionamento para uma trusted
surface para ser concluído.
* Resolver o desafio: o usuário deve ter uma forma de resolver o desafio em uma
trusted surface (por exemplo, aplicativo do banco, site etc.)
* Autorizar a transação: o emissor aprova o pagamento e confirma o sucesso. Isso
é comunicado ao usuário e ao Merchant para que o pedido possa ser atendido. Um
comprovante de pagamento é compartilhado com o Credential Provider, confirmando
o resultado da transação. Em caso de recusa, isso também pode ser comunicado de
forma adequada.

### 4.2 Transação human-not-present

O humano delega a um agente de IA uma tarefa que exige um pagamento (por
exemplo, uma compra) e quer que o agente de IA faça o pagamento na sua ausência.
Alguns cenários típicos seriam “*compre estes tênis para mim quando o preço
cair abaixo de US$ 100*” ou “*compre 2 ingressos para este show assim que
estiverem disponíveis, garanta que fiquemos perto do palco principal, mas não
gaste mais de US$ 1000*”.

As principais diferenças em relação à modalidade human-present estão abaixo:

* O agente precisa repetir ao usuário o que entende que deve comprar. O usuário
precisa aprovar isso e confirmar que quer que o agente faça a compra na sua
ausência. Para isso, o usuário passa por uma autenticação na sessão (biometria
etc.) para confirmar sua intenção.
* O “Checkout Mandate” assinado pelo usuário passa a conter a lista de condições
em que o SA pode atender ao pedido do usuário. Esse mandate fica no estado
“Open” (aberto) enquanto o agente tenta atender aos requisitos do usuário.
Quando o SA determina que os requisitos podem ser atendidos, o mandate passa
para “Closed” (fechado).
* O Merchant pode exigir confirmação do usuário: se o Merchant não tiver certeza
de que consegue atender às necessidades do usuário (por exemplo, o pedido não é
para um SKU específico), ele pode exigir que o usuário volte à sessão para
confirmar as condições de compra ou fornecer informações adicionais.
