# language: pt
@v4 @F-V4.3.1
Funcionalidade: Spike: publicação do ADK Web atrás do nginx
  PBI F-V4.3.1 · Spike: forma de publicar o ADK Web atrás do nginx

  Contexto:
    Dado que a prova de conceito do spike está publicada no Space da v4

  @CT01 @positivo
  # Origem: CA2
  Cenário: CT01 · ADK Web abre pelo Space
    Quando um visitante abre https://ds-fabiopinheiro-ap2-homolog-v4.hf.space/dev-ui (ou o caminho definido no spike)
    Então a tela do ADK Web é exibida

  @CT02 @positivo
  # Origem: CA1 / RN01
  Cenário: CT02 · Decisão registrada
    Quando o CLAUDE.md do branch homolog-v4 é revisado
    Então existe uma seção de decisão com pelo menos 2 alternativas, riscos e a alternativa escolhida
