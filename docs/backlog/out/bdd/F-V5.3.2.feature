# language: pt
@v5 @F-V5.3.2
Funcionalidade: Forma de pagamento e assinatura do Payment Mandate na Trusted Surface
  PBI F-V5.3.2 · Escolha da forma de pagamento e assinatura do Payment Mandate na Trusted Surface

  Contexto:
    Dado que o usuário escolheu uma opção de compra de US$ 450,00 em https://ap2-homolog-v5-frontend.vercel.app

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Formas de pagamento da conta de demonstração
    Quando a etapa de forma de pagamento é exibida
    Então a lista contém "American Express ending in 4444"

  @CT02 @positivo
  # Origem: CA2 / RN01
  Cenário: CT02 · Trusted Surface mostra os dados da compra
    Dado que o usuário escolheu "American Express ending in 4444"
    Quando a Trusted Surface é exibida
    Então ela mostra o item, o valor US$ 450,00, o comerciante e a forma de pagamento

  @CT03 @negativo
  # Origem: CA3 / RN02
  Cenário: CT03 · Recusa na Trusted Surface
    Dado que a Trusted Surface está exibida
    Quando o usuário clica em "Recusar"
    Então a compra é encerrada
    E nenhum Payment Mandate aparece na aba Mandates

  @CT04 @positivo
  # Origem: CA4
  Cenário: CT04 · Assinatura gera o Payment Mandate
    Dado que a Trusted Surface está exibida
    Quando o usuário clica em "Aprovar e assinar"
    Então o Payment Mandate aparece na aba Mandates

  @CT05 @seguranca
  # Origem: RN01
  Cenário: CT05 · Valor assinado igual ao valor exibido
    Dado que a Trusted Surface exibiu o valor US$ 450,00
    Quando o usuário clica em "Aprovar e assinar"
    Então o Payment Mandate decodificado na aba Mandates tem o valor 45000 centavos em USD

  @CT06 @negativo
  # Origem: RN02
  Cenário: CT06 · Página recarregada antes da assinatura
    Dado que a Trusted Surface está exibida
    Quando o usuário recarrega a página
    Então nenhum pagamento é iniciado
