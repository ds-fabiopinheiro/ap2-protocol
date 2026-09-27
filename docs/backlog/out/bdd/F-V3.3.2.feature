# language: pt
@v3 @F-V3.3.2
Funcionalidade: Modelo dos agentes A2A definido por AGENT_MODEL
  PBI F-V3.3.2 · Modelo dos agentes A2A definido por AGENT_MODEL

  Contexto:
    Dado que o Space da v3 tem GOOGLE_API_KEY e VERCEL_AI_GATEWAY_API_KEY cadastrados

  @CT01 @positivo
  # Origem: CA1 / CA2 / RN01 / RN02
  Esquema do Cenário: CT01 · Cliente usado conforme o nome do modelo
    Dado que AGENT_MODEL é <modelo>
    Quando o Space inicia e o script de F-V3.2.2 (CT01) é executado
    Então o log dos agentes A2A mostra o cliente <cliente>
    E o script imprime "OK"

    Exemplos:
      | modelo                                                 | cliente       |
      | gemini-3.1-flash-lite-preview                          | Gemini nativo |
      | vercel_ai_gateway/google/gemini-3.1-flash-lite-preview | LiteLLM       |

  @CT02 @borda
  # Origem: RN02 (F-V3.3)
  Cenário: CT02 · AGENT_MODEL ausente usa o padrão
    Dado que a variável AGENT_MODEL não existe no Space
    Quando o Space inicia
    Então o log dos agentes A2A mostra o modelo "gemini-3.1-flash-lite-preview"

  @CT03 @negativo
  # Origem: CA3
  Cenário: CT03 · Modelo inválido
    Dado que AGENT_MODEL é "modelo-inexistente"
    Quando o script de F-V3.2.2 é executado
    Então o log dos agentes A2A mostra erro de modelo não encontrado
    E o agent card do Merchant Agent continua retornando HTTP 200

  @CT04 @regressao
  # Origem: RN03
  Cenário: CT04 · Troca de modelo na v3 não altera a v2
    Dado que AGENT_MODEL da v3 é "vercel_ai_gateway/google/gemini-3.1-flash-lite-preview"
    Quando a compra autônoma da v2 é executada
    Então a compra é concluída
    E o log da v2 mostra "AGENT_MODEL=gemini-3.1-flash-lite-preview"

  @CT05 @negativo
  # Origem: CA4 / CA5 / RN04
  Esquema do Cenário: CT05 · Nova tentativa em erro temporário do modelo
    Dado que a chamada ao modelo retorna <respostas> em sequência (simulado em teste unitário)
    Quando o Merchant Agent processa um pedido
    Então o resultado é <resultado>
    E o número de chamadas ao modelo é <chamadas>

    Exemplos:
      | respostas     | resultado       | chamadas |
      | 503, 200      | resposta normal | 2        |
      | 503, 503, 200 | resposta normal | 3        |
      | 503, 503, 503 | erro legível    | 3        |
      | 400           | erro legível    | 1        |
