# language: pt
@v5 @F-V5.3.1
Funcionalidade: Seleção das opções de compra do Merchant
  PBI F-V5.3.1 · Seleção das opções de compra do Merchant

  Contexto:
    Dado que o usuário está em https://ap2-homolog-v5-frontend.vercel.app na "Compra assistida"

  @CT01 @positivo
  # Origem: CA1 / RN01
  Cenário: CT01 · Opções exibidas com os dados do Merchant
    Quando o usuário envia "I want to buy a coffee maker" e o Merchant devolve 3 opções
    Então a tela mostra 3 cartões, cada um com nome, preço e comerciante

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Escolha de uma opção avança o fluxo
    Dado que a tela mostra as opções de compra
    Quando o usuário escolhe a primeira opção
    Então a escolha é enviada ao Shopping Agent v1
    E a etapa de forma de pagamento é exibida

  @CT03 @borda
  # Origem: CA3
  Cenário: CT03 · Nenhuma opção retornada
    Quando o Merchant devolve 0 opções
    Então a tela mostra mensagem de que não há opções
    E o usuário pode enviar um novo pedido

  @CT04 @borda
  # Origem: RN02
  Cenário: CT04 · Apenas uma opção pode ser escolhida
    Dado que o usuário escolheu a primeira opção
    Quando tenta escolher a segunda opção
    Então a seleção da segunda opção não é enviada ao agente

  @CT05 @borda
  # Origem: RN03 (F-V5.3)
  Esquema do Cenário: CT05 · Formato de preço em dólar
    Quando o Merchant devolve uma opção com preço <valor> USD
    Então a tela exibe <exibido>

    Exemplos:
      | valor  | exibido      |
      | 450    | US$ 450,00   |
      | 1234.5 | US$ 1.234,50 |
      | 0.99   | US$ 0,99     |
