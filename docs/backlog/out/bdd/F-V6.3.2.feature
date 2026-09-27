# language: pt
@v6 @F-V6.3.2
Funcionalidade: APK de homologação publicado no GitHub Releases
  PBI F-V6.3.2 · APK de homologação publicado no GitHub Releases

  Contexto:
    Dado que o workflow de build do APK existe no branch homolog-v6

  @CT01 @positivo
  # Origem: CA1 / RN01
  Cenário: CT01 · Tag gera o APK na release
    Quando a tag v6.0.1 é enviada ao repositório
    Então a release "v6.0.1" contém um arquivo APK com "6.0.1" no nome

  @CT02 @negativo
  # Origem: RN01
  Cenário: CT02 · Push sem tag não publica release
    Quando um commit é enviado ao branch homolog-v6 sem tag
    Então nenhuma release nova é criada

  @CT03 @positivo
  # Origem: CA2
  Cenário: CT03 · Instalação em aparelho físico
    Dado um aparelho Android 8.0 ou superior (minSdk 26) com instalação de fontes externas permitida
    Quando o APK da release é instalado
    Então o app abre na tela inicial

  @CT04 @positivo
  # Origem: CA3
  Cenário: CT04 · Compra com Digital Payment Credential
    Dado um aparelho físico compatível com Credential Manager e DPC
    Quando o usuário conclui uma compra no app e autoriza com a credencial digital
    Então o app mostra a confirmação da compra
