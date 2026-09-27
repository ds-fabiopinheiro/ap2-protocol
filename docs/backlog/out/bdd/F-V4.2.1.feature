# language: pt
@v4 @F-V4.2.1
Funcionalidade: Credentials Provider Agent lista as formas de pagamento da conta de demonstração
  PBI F-V4.2.1 · Credentials Provider Agent lista as formas de pagamento da conta de demonstração

  Contexto:
    Dado que o Space da v4 está em "Running"
    E a conta de demonstração de account_manager.py está carregada

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Lista de formas de pagamento da demo
    Quando o Shopping Agent v1 pede as formas de pagamento da conta de demonstração
    Então a lista contém "American Express ending in 4444"

  @CT02 @negativo
  # Origem: CA2
  Cenário: CT02 · Credentials Provider fora do ar
    Dado que o processo do Credentials Provider Agent está parado
    Quando o usuário chega à etapa de forma de pagamento no ADK Web
    Então a conversa informa que não foi possível obter as formas de pagamento

  @CT03 @seguranca
  # Origem: RN01 (F-V4.2)
  Cenário: CT03 · Credentials Provider não é acessível de fora
    Quando é feito GET https://ds-fabiopinheiro-ap2-homolog-v4.hf.space/a2a/credentials_provider/.well-known/agent-card.json
    Então a resposta é HTTP 404

  @CT04 @positivo
  # Origem: Task: espelhamento no Supabase
  Cenário: CT04 · Estado mantido após restart
    Dado que uma forma de pagamento foi usada em uma compra da v4
    Quando o Space da v4 é reiniciado
    Então o log mostra restore com environment='v4'
    E a próxima compra usa a mesma conta de demonstração
