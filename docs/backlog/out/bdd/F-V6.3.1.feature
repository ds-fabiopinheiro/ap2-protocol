# language: pt
@v6 @F-V6.3.1
Funcionalidade: App Android usando o backend público sem chave no APK
  PBI F-V6.3.1 · App Android configurado para o backend público sem chave no APK

  Contexto:
    Dado que o APK de homologação da v6 está instalado em um aparelho físico com internet

  @CT01 @positivo
  # Origem: CA1 / RN01
  Cenário: CT01 · App conecta ao Space por HTTPS
    Quando o usuário envia "I want to buy a coffee maker" no app
    Então as requisições ao Merchant vão para https://ds-fabiopinheiro-ap2-homolog-v6.hf.space por HTTPS
    E o app mostra as opções de compra

  @CT02 @seguranca
  # Origem: CA2 / RN01 (F-V6.3)
  Cenário: CT02 · APK sem chave do Gemini
    Dado o arquivo APK publicado
    Quando o APK é descompactado e é feita a busca pelo padrão de chave do Google ("AIza")
    Então nenhuma ocorrência é encontrada

  @CT03 @negativo
  # Origem: CA3
  Cenário: CT03 · Backend fora do ar
    Dado que o Space da v6 está parado
    Quando o usuário envia uma mensagem no app
    Então o app mostra erro de conexão

  @CT04 @seguranca
  # Origem: RN02 (F-V6.3)
  Cenário: CT04 · Conexão sem HTTPS é recusada
    Dado que a URL do Merchant no build é "http://ds-fabiopinheiro-ap2-homolog-v6.hf.space/a2a/merchant_agent"
    Quando o usuário envia uma mensagem no app
    Então o app não envia a requisição e mostra erro de configuração

  @CT05 @seguranca
  # Origem: RN02
  Cenário: CT05 · Limite de requisições no proxy do Gemini
    Dado que o proxy do Gemini tem limite de <limite> requisições por minuto por visitante
    Quando o mesmo aparelho envia <limite>+1 requisições em 1 minuto
    Então a última resposta é HTTP 429
