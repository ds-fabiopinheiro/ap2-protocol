# language: pt
@v3 @F-V3.2.1
Funcionalidade: Merchant Agent acessível por A2A com agent card público
  PBI F-V3.2.1 · Merchant Agent acessível por A2A com agent card público

  Contexto:
    Dado que o Space da v3 está em "Running" em https://ds-fabiopinheiro-ap2-homolog-v3.hf.space

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Agent card público do Merchant Agent
    Quando é feito GET https://ds-fabiopinheiro-ap2-homolog-v3.hf.space/a2a/merchant_agent/.well-known/agent-card.json
    Então a resposta é HTTP 200 com Content-Type application/json

  @CT02 @positivo
  # Origem: CA1 / RN01
  Cenário: CT02 · URL do agent card aponta para o Space
    Quando o agent card do Merchant Agent é consultado
    Então o campo "url" é "https://ds-fabiopinheiro-ap2-homolog-v3.hf.space/a2a/merchant_agent"

  @CT03 @negativo
  # Origem: CA2
  Cenário: CT03 · Queda do Merchant Agent reinicia o container
    Dado que o processo do Merchant Agent é encerrado dentro do container
    Quando o Hugging Face reinicia o Space
    Então o agent card do Merchant Agent volta a retornar HTTP 200

  @CT04 @borda
  # Origem: CA3 / RN02
  Esquema do Cenário: CT04 · Limite de requisições por visitante
    Dado que o limite da rota é 20 requisições/min com rajada de 10
    Quando o mesmo visitante envia <total> requisições simultâneas ao agent card
    Então <aceitas> respostas têm HTTP 200
    E <recusadas> respostas têm HTTP 429

    Exemplos:
      | total | aceitas | recusadas |
      | 11    | 11      | 0         |
      | 12    | 11      | 1         |
      | 15    | 11      | 4         |

  @CT05 @seguranca
  # Origem: CA3
  Cenário: CT05 · Resposta 429 legível pelo navegador
    Dado que o visitante já excedeu o limite da rota /a2a/merchant_agent
    Quando envia mais uma requisição com Origin https://ap2-homolog-v5-frontend.vercel.app
    Então o corpo da resposta 429 contém "rate_limited"
    E o cabeçalho Access-Control-Allow-Origin é "*"

  @CT06 @regressao
  # Origem: CA4
  Cenário: CT06 · Shopping Agent v2 continua no Space da v3
    Quando é feito GET https://ds-fabiopinheiro-ap2-homolog-v3.hf.space/a2a/shopping_agent/.well-known/agent-card.json
    Então a resposta é HTTP 200
