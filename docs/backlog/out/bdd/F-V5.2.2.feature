# language: pt
@v5 @F-V5.2.2
Funcionalidade: Escolha entre jornada autônoma e assistida
  PBI F-V5.2.2 · Escolha entre jornada autônoma e assistida na tela inicial

  Contexto:
    Dado que o usuário abre https://ap2-homolog-v5-frontend.vercel.app

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Tela inicial com as duas jornadas
    Quando a página termina de carregar
    Então a tela mostra as opções "Compra autônoma" e "Compra assistida" com uma descrição curta de cada

  @CT02 @positivo
  # Origem: CA2 / RN02 (F-V5.2)
  Cenário: CT02 · Jornada assistida usa o Shopping Agent v1
    Dado que o usuário escolheu "Compra assistida"
    Quando envia a mensagem "I want to buy a coffee maker"
    Então a requisição A2A é enviada para a URL de VITE_ASSISTED_AGENT_URL

  @CT03 @positivo
  # Origem: CA3 / RN02
  Cenário: CT03 · Troca de jornada pede confirmação
    Dado que o usuário está numa conversa da "Compra assistida"
    Quando escolhe "Compra autônoma"
    Então a tela pede confirmação para iniciar nova conversa

  @CT04 @positivo
  # Origem: CA3 / RN02
  Cenário: CT04 · Troca confirmada inicia nova sessão
    Dado que a tela pediu confirmação de troca de jornada
    Quando o usuário confirma
    Então a conversa anterior some da tela
    E a próxima mensagem é enviada com um sessionId diferente do anterior

  @CT05 @negativo
  # Origem: RN01
  Cenário: CT05 · Troca cancelada mantém a conversa
    Dado que a tela pediu confirmação de troca de jornada
    Quando o usuário cancela
    Então a conversa atual continua exibida na mesma jornada

  @CT06 @negativo
  # Origem: CA (F-V5.2)
  Cenário: CT06 · Agente da jornada assistida fora do ar
    Dado que o Shopping Agent v1 da v5 não responde
    Quando o usuário envia uma mensagem na "Compra assistida"
    Então a tela mostra uma mensagem iniciada por "Erro de conexão"
    E a opção "Compra autônoma" continua disponível

  @CT07 @regressao
  # Origem: RN01 (F-V5.2)
  Cenário: CT07 · Compra autônoma no web client da v5
    Dado que o usuário escolheu "Compra autônoma"
    Quando executa o roteiro de compra autônoma com price drop price=199 e stock=10
    Então a tela mostra "Compra concluída" com valor US$ 199,00
