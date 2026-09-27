# language: pt
@v3 @F-V3.2.2
Funcionalidade: Busca de produto no Merchant Agent com resposta assinada
  PBI F-V3.2.2 · Busca de produto no Merchant Agent com resposta assinada

  Contexto:
    Dado que o Merchant Agent da v3 está publicado
    E o script deploy/tests/merchant_a2a_test.py está configurado com a URL do Space da v3

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Pedido de produto retorna opções assinadas
    Quando o script envia a intenção de compra "coffee maker" com a extensão AP2
    Então a resposta contém pelo menos 1 opção de compra
    E cada opção contém uma assinatura do Merchant

  @CT02 @positivo
  # Origem: CA2 / RN02
  Cenário: CT02 · Assinatura válida é aceita pelo script
    Dado uma resposta recebida do Merchant Agent
    Quando o script verifica a assinatura com a chave pública do Merchant
    Então o script imprime "OK" e termina com código 0

  @CT03 @negativo
  # Origem: CA3 / RN02
  Cenário: CT03 · Assinatura alterada é recusada pelo script
    Dado uma resposta recebida do Merchant Agent com 1 byte da assinatura alterado
    Quando o script verifica a assinatura
    Então o script imprime "FALHA" e termina com código diferente de 0

  @CT04 @positivo
  # Origem: CA4
  Cenário: CT04 · Mandates registrados no Supabase da v3
    Dado que o CT01 foi executado às <hora_do_teste>
    Quando é consultado ap2_env_mandates com environment='v3' e first_seen_at posterior a <hora_do_teste>
    Então existe pelo menos 1 linha

  @CT05 @negativo
  # Origem: RN01
  Cenário: CT05 · Mensagem sem a extensão AP2
    Quando o script envia a intenção "coffee maker" sem declarar a extensão AP2 (EXTENSION_URI)
    Então o Merchant Agent responde com erro e não devolve opção assinada

  @CT06 @performance
  # Origem: Métrica do épico
  Cenário: CT06 · Consumo do Gemini em 3 execuções seguidas
    Dado que nenhum outro teste usa a GOOGLE_API_KEY no período
    Quando o CT01 é executado 3 vezes seguidas
    Então o pico de RPM no AI Studio para gemini-3.1-flash-lite-preview é menor que 15
