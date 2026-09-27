# language: pt
@v5 @F-V5.3.3
Funcionalidade: Desafio OTP e recibo da compra assistida
  PBI F-V5.3.3 · Desafio OTP e recibo da compra assistida

  Contexto:
    Dado que o usuário assinou o Payment Mandate de US$ 450,00 em https://ap2-homolog-v5-frontend.vercel.app
    E a tela mostra o desafio OTP

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · OTP correto mostra o recibo
    Quando o usuário informa "123" e confirma
    Então a tela mostra o recibo com número do pedido, valor US$ 450,00 e forma de pagamento

  @CT02 @negativo
  # Origem: CA2
  Cenário: CT02 · OTP errado permite nova tentativa
    Quando o usuário informa "000" e confirma
    Então a tela mostra erro de OTP inválido
    E o campo de OTP continua disponível

  @CT03 @borda
  # Origem: RN01
  Esquema do Cenário: CT03 · Campo OTP aceita só dígitos
    Quando o usuário digita <entrada> no campo OTP
    Então o botão de confirmar fica <estado>

    Exemplos:
      | entrada    | estado       |
      | "123"      | habilitado   |
      | "12a"      | desabilitado |
      | "" (vazio) | desabilitado |

  @CT04 @negativo @pendente-confirmacao
  # Origem: CA3 / RN02 (proposta)
  Cenário: CT04 · Três OTPs errados encerram a compra
    Dado que o usuário informou "000" duas vezes
    Quando informa "000" pela terceira vez
    Então a compra é encerrada
    E nenhum recibo é exibido
