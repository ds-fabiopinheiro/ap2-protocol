# language: pt
@v3 @F-V3.3.1
Funcionalidade: Merchant Payment Processor Agent em execução interna
  PBI F-V3.3.1 · Merchant Payment Processor Agent em execução interna com desafio OTP

  Contexto:
    Dado que o Space da v3 está em "Running"

  @CT01 @positivo
  # Origem: CA1 / RN01
  Cenário: CT01 · Processor responde dentro do container
    Quando é feito GET http://127.0.0.1:8003/a2a/merchant_payment_processor_agent/.well-known/agent-card.json dentro do container
    Então a resposta é HTTP 200

  @CT02 @seguranca
  # Origem: CA2 / RN01
  Cenário: CT02 · Processor não é acessível de fora
    Quando é feito GET https://ds-fabiopinheiro-ap2-homolog-v3.hf.space/a2a/merchant_payment_processor_agent/.well-known/agent-card.json
    Então a resposta é HTTP 404

  @CT03 @negativo
  # Origem: CA3
  Cenário: CT03 · Queda do Processor reinicia o container
    Dado que o processo do Processor Agent é encerrado
    Quando o Hugging Face reinicia o Space
    Então o agent card local do Processor volta a retornar HTTP 200
