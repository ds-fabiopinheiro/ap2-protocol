# language: pt
@v6 @F-V6.2.2
Funcionalidade: Compra assistida com backend Go
  PBI F-V6.2.2 · Compra assistida com backend Go

  Contexto:
    Dado que o Space da v6 está com AP2_BACKEND_LANG=go
    E o usuário está na "Compra assistida" do web client apontado para a v6

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Compra concluída com backend Go
    Dado que o usuário escolheu uma opção e "American Express ending in 4444" e assinou o Payment Mandate
    Quando informa o OTP "123"
    Então a tela mostra o recibo da compra

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Mandates registrados na v6
    Dado que o CT01 foi concluído às <hora_do_teste>
    Quando é consultado ap2_env_mandates com environment='v6' e first_seen_at posterior a <hora_do_teste>
    Então existe o Payment Mandate da compra

  @CT03 @negativo
  # Origem: RN01 (mesmo roteiro da v4/v5)
  Cenário: CT03 · OTP errado com backend Go
    Quando o usuário informa o OTP "000"
    Então o pagamento não é concluído
