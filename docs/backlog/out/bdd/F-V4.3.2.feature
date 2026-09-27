# language: pt
@v4 @F-V4.3.2
Funcionalidade: Compra assistida ponta a ponta pelo ADK Web
  PBI F-V4.3.2 · Compra assistida ponta a ponta pelo ADK Web

  Contexto:
    Dado que o ADK Web da v4 está aberto com o agente shopping_agent selecionado
    E Merchant, Credentials Provider e Processor Agents estão em execução

  @CT01 @positivo
  # Origem: CA1 / RN02
  Cenário: CT01 · Compra assistida concluída
    Dado que o usuário pediu "I want to buy a coffee maker" e escolheu uma das opções
    E escolheu a forma de pagamento "American Express ending in 4444" e assinou o Payment Mandate
    Quando informa o OTP "123"
    Então a conversa mostra a confirmação da compra com o recibo

  @CT02 @negativo
  # Origem: CA2 / RN02
  Cenário: CT02 · OTP incorreto
    Dado que o usuário chegou ao desafio OTP
    Quando informa o OTP "000"
    Então o pagamento não é concluído
    E a conversa informa que o OTP é inválido

  @CT03 @negativo
  # Origem: CA3 / RN01
  Cenário: CT03 · Usuário recusa o carrinho
    Dado que o Merchant apresentou as opções de compra
    Quando o usuário responde que não quer nenhuma delas
    Então nenhum Payment Mandate é criado em ap2_env_mandates com environment='v4'

  @CT04 @positivo
  # Origem: CA4 / RN03
  Cenário: CT04 · Mandates da compra registrados
    Dado que o CT01 foi concluído às <hora_do_teste>
    Quando é consultado ap2_env_mandates com environment='v4' e first_seen_at posterior a <hora_do_teste>
    Então existe o Payment Mandate da compra

  @CT05 @seguranca
  # Origem: RN01 (F-V4.3)
  Cenário: CT05 · ADK Web lista só o Shopping Agent v1
    Quando o visitante abre o seletor de agentes do ADK Web
    Então a lista contém apenas "shopping_agent"

  @CT06 @performance
  # Origem: Métrica do épico
  Cenário: CT06 · Consumo do Gemini em uma compra assistida
    Dado que nenhum outro teste usa a GOOGLE_API_KEY no período
    Quando o CT01 é executado 1 vez
    Então o pico de RPM no AI Studio é menor que 15

  @CT07 @negativo
  # Origem: CA5
  Cenário: CT07 · Erro 503 temporário no Shopping Agent v1
    Dado que a primeira chamada do Shopping Agent v1 ao modelo retorna 503 (simulado em teste unitário)
    Quando o usuário envia "I want to buy a coffee maker"
    Então a conversa continua com as opções de compra após a nova tentativa
