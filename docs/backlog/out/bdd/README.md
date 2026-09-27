# Cenários de teste (BDD) — backlog v3–v6

Preview gerado a partir dos critérios de aceite e das regras de negócio de cada PBI. Nada foi vinculado a Test Plan ou criado no GitHub.

**Parâmetros usados:** tipos positivo, negativo, borda e, quando há requisito ou risco declarado, segurança, performance e regressão · idioma pt-BR · formato Gherkin (`# language: pt`) · um arquivo `.feature` por PBI.

**Tags:** `@vN` (versão), `@<PBI>`, `@CTnn`, tipo (`@positivo`, `@negativo`, `@borda`, `@seguranca`, `@performance`, `@regressao`) e `@pendente-confirmacao` para cenários que dependem de regra ainda não confirmada.

## Resumo

| Versão | PBI | Cenários | Positivo | Negativo | Borda | Segurança | Performance | Regressão | CA sem cenário |
|---|---|---|---|---|---|---|---|---|---|
| v3 | F-V3.1.1 | 7 | 3 | 2 | 0 | 1 | 0 | 1 | 0 |
| v3 | F-V3.2.1 | 6 | 2 | 1 | 1 | 1 | 0 | 1 | 0 |
| v3 | F-V3.2.2 | 6 | 3 | 2 | 0 | 0 | 1 | 0 | 0 |
| v3 | F-V3.3.1 | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| v3 | F-V3.3.2 | 5 | 1 | 2 | 1 | 0 | 0 | 1 | 0 |
| v4 | F-V4.1.1 | 7 | 3 | 2 | 0 | 1 | 0 | 1 | 0 |
| v4 | F-V4.2.1 | 4 | 2 | 1 | 0 | 1 | 0 | 0 | 0 |
| v4 | F-V4.3.1 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| v4 | F-V4.3.2 | 7 | 2 | 3 | 0 | 1 | 1 | 0 | 0 |
| v5 | F-V5.1.1 | 8 | 4 | 2 | 0 | 1 | 0 | 1 | 0 |
| v5 | F-V5.2.1 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| v5 | F-V5.2.2 | 7 | 4 | 2 | 0 | 0 | 0 | 1 | 0 |
| v5 | F-V5.3.1 | 5 | 2 | 0 | 3 | 0 | 0 | 0 | 0 |
| v5 | F-V5.3.2 | 6 | 3 | 2 | 0 | 1 | 0 | 0 | 0 |
| v5 | F-V5.3.3 | 4 | 1 | 2 | 1 | 0 | 0 | 0 | 0 |
| v6 | F-V6.1.1 | 7 | 3 | 2 | 0 | 1 | 0 | 1 | 0 |
| v6 | F-V6.2.1 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| v6 | F-V6.2.2 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| v6 | F-V6.3.1 | 5 | 1 | 1 | 0 | 3 | 0 | 0 | 0 |
| v6 | F-V6.3.2 | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 |

Total: 101 cenários em 20 PBIs. CA sem cenário: 0.

## Preview — Cenários de teste · PBI F-V3.1.1 Ambiente de homologação v3 publicado a partir do branch homolog-v3

Arquivo: `out/bdd/F-V3.1.1.feature` · 7 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O Space ds-fabiopinheiro/ap2-homolog-v3 fica em estado Running a partir do branch homolog-v3. | Critério de aceite | CT01 |
| CA2 – Um push de backend em homolog-v3 reconstrói apenas ds-fabiopinheiro/ap2-homolog-v3. | Critério de aceite | CT02 |
| CA3 – Após restart do Space da v3, o log mostra restore apenas de arquivos com environment='v3'. | Critério de aceite | CT04 |
| CA4 – A v2 (homolog-deploy) e as versões anteriores passam no roteiro de regressão depois da criação da nova versão. | Critério de aceite | CT05 |
| CA5 – Se o secret GOOGLE_API_KEY estiver ausente, o log de inicialização mostra o aviso e o agent card continua respondendo. | Critério de aceite | CT06 |
| RN01 – Todo trabalho da v3 entra por PR no branch homolog-v3; o branch homolog-deploy não recebe código da v3. | Regra de negócio do PBI | — |
| RN02 – O estado da v3 no Supabase fica separado das outras versões (AP2_ENV=v3). | Regra de negócio do PBI | CT04 |
| RN03 – Nenhum segredo é gravado no repositório, em variável VITE_* ou em variável pública do Space. | Regra de negócio do PBI | CT07 |
| RN do workflow (paths) | Regra da feature/épico ou task | CT03 |
| RN03 | Regra da feature/épico ou task | CT07 |

### Cenários

```gherkin
# language: pt
@v3 @F-V3.1.1
Funcionalidade: Ambiente de homologação v3 (homolog-v3)
  PBI F-V3.1.1 · Ambiente de homologação v3 publicado a partir do branch homolog-v3

  Contexto:
    Dado que o branch homolog-v3 foi criado a partir de homolog-deploy

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Space da v3 publicado a partir do branch homolog-v3
    Dado que o Space ds-fabiopinheiro/ap2-homolog-v3 está configurado com AP2_REF=homolog-v3 e AP2_ENV=v3
    Quando o build do Space termina
    Então o estado exibido no Hugging Face é "Running"
    E GET https://ds-fabiopinheiro-ap2-homolog-v3.hf.space/a2a/shopping_agent/.well-known/agent-card.json retorna HTTP 200

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Push de backend em homolog-v3 reconstrói só o Space da v3
    Dado que os Spaces da v2 e da v3 estão em "Running"
    Quando um commit que altera deploy/hf-space/start.sh é enviado ao branch homolog-v3
    Então o workflow "HF Space rebuild" executa Factory rebuild de ds-fabiopinheiro/ap2-homolog-v3
    E o Space ds-fabiopinheiro/ap2-homolog-backend continua em "Running" sem rebuild

  @CT03 @negativo
  # Origem: RN do workflow (paths)
  Cenário: CT03 · Push só de documentação não dispara rebuild
    Dado que o Space da v3 está em "Running"
    Quando um commit que altera apenas CLAUDE.md é enviado ao branch homolog-v3
    Então o workflow "HF Space rebuild" não é executado

  @CT04 @positivo
  # Origem: CA3 / RN02
  Cenário: CT04 · Restore lê apenas o estado da v3
    Dado que ap2_env_state_files tem 3 arquivos com environment='v3' e 2 arquivos com environment='outra'
    Quando o Space da v3 é reiniciado
    Então o log de inicialização mostra "restored 3 file(s)"
    E nenhum arquivo de environment='outra' aparece em TEMP_DB_DIR

  @CT05 @regressao
  # Origem: CA4
  Cenário: CT05 · Compra autônoma da v2 continua funcionando após a criação da v3
    Dado que a v3 está publicada
    E o web client da v2 está aberto em https://ap2-homolog-frontend.vercel.app
    Quando o usuário aprova o mandate de um item com orçamento US$ 500 e o price drop é disparado com price=199 e stock=10
    Então a tela da v2 mostra "Compra concluída" com valor US$ 199,00
    E a tabela ap2_mandates da v2 recebe 4 novas linhas

  @CT06 @negativo
  # Origem: CA5
  Cenário: CT06 · Space inicia sem GOOGLE_API_KEY
    Dado que o Space da v3 não tem o secret GOOGLE_API_KEY
    Quando o Space inicia
    Então o log mostra "WARNING: GOOGLE_API_KEY is not set"
    E o agent card público retorna HTTP 200

  @CT07 @seguranca
  # Origem: RN03
  Cenário: CT07 · Nenhum segredo no branch da versão
    Dado o conteúdo do branch homolog-v3
    Quando a varredura de segredos (gitleaks) é executada em todo o histórico do branch
    Então nenhum segredo é encontrado
```

### Lacunas identificadas
- Não está definido o comportamento de um Space ≠ v2 iniciado sem AP2_ENV: hoje o sync usaria as tabelas da v2. Sugestão: o start.sh encerrar com erro quando AP2_REF ≠ homolog-deploy e AP2_ENV estiver vazio.

### Premissas
- Nome dos Spaces e URLs seguem o padrão ds-fabiopinheiro/ap2-homolog-vN.
- gitleaks disponível no CI ou na máquina de quem testa.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V3.2.1 Merchant Agent acessível por A2A com agent card público

Arquivo: `out/bdd/F-V3.2.1.feature` · 6 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O agent card público retorna 200 e o campo url aponta para o Space da v3. | Critério de aceite | CT01, CT02 |
| CA2 – Se o Merchant Agent cair, o container reinicia (mesmo comportamento da v2). | Critério de aceite | CT03 |
| CA3 – Requisições acima do limite recebem 429 com corpo JSON e cabeçalho CORS. | Critério de aceite | CT04, CT05 |
| CA4 – A rota /a2a/shopping_agent da v2 continua funcionando no Space da v3. | Critério de aceite | CT06 |
| RN01 – A URL do agent card é reescrita para https://$SPACE_HOST/a2a/merchant_agent na inicialização. | Regra de negócio do PBI | CT02 |
| RN02 – Limite de 20 requisições/min por visitante e 120/min no total na rota /a2a/merchant_agent. | Regra de negócio do PBI | CT04 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- O Space da v3 herda do nginx da v2 os valores de limite (20/min por visitante, rajada 10, nodelay).
- O visitante é identificado pelo último IP do X-Forwarded-For, como na v2.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V3.2.2 Busca de produto no Merchant Agent com resposta assinada

Arquivo: `out/bdd/F-V3.2.2.feature` · 6 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O script de teste envia a intenção de compra e recebe pelo menos uma opção assinada. | Critério de aceite | CT01 |
| CA2 – O script verifica a assinatura e imprime OK. | Critério de aceite | CT02 |
| CA3 – Com assinatura alterada, o script imprime FALHA e sai com código diferente de zero. | Critério de aceite | CT03 |
| CA4 – Os mandates gerados aparecem em ap2_env_mandates com environment='v3'. | Critério de aceite | CT04 |
| RN01 – O teste usa só mensagens A2A com a extensão AP2 (EXTENSION_URI). | Regra de negócio do PBI | CT05 |
| RN02 – O teste falha se a assinatura do Merchant não verificar com a chave pública publicada. | Regra de negócio do PBI | CT02, CT03 |
| Métrica do épico | Regra da feature/épico ou task | CT06 |
| RN01 | Regra da feature/épico ou task | CT05 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Comportamento para produto que o Merchant não conhece não está definido no repositório; não há cenário.

### Premissas
- O retorno de erro no CT05 depende de o Merchant exigir a extensão AP2 (required_extensions em remote_agents.py sugere que sim); confirmar.
- "coffee maker" é o exemplo do README do cenário human-present.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V3.3.1 Merchant Payment Processor Agent em execução interna com desafio OTP

Arquivo: `out/bdd/F-V3.3.1.feature` · 3 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O agent card local em 127.0.0.1:8003 responde 200. | Critério de aceite | CT01 |
| CA2 – Uma requisição externa ao Processor recebe 404. | Critério de aceite | CT02 |
| CA3 – Se o Processor cair, o container reinicia. | Critério de aceite | CT03 |
| RN01 – Acesso apenas por 127.0.0.1:8003. | Regra de negócio do PBI | CT01, CT02 |
| RN02 – O OTP de demonstração é 123. | Regra de negócio do PBI | — |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- O desafio OTP (RN02) só pode ser exercitado com o Shopping Agent v1; está coberto em F-V4.3.2 (CT01 e CT02).

### Premissas
- O teste interno (CT01) é feito pelo terminal do Space (Dev Mode) ou por log de health check.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V3.3.2 Modelo dos agentes A2A definido por AGENT_MODEL

Arquivo: `out/bdd/F-V3.3.2.feature` · 5 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Com AGENT_MODEL=gemini-3.1-flash-lite-preview, o teste de F-V3.2.2 passa. | Critério de aceite | CT01 |
| CA2 – Com AGENT_MODEL de outro provedor e a chave correspondente, o teste de F-V3.2.2 passa. | Critério de aceite | CT01 |
| CA3 – Com AGENT_MODEL inválido, o log mostra erro claro e o agent card continua respondendo. | Critério de aceite | CT03 |
| CA4 – Com um 503 simulado na primeira chamada ao modelo, a requisição é concluída na nova tentativa. | Critério de aceite | CT05 |
| CA5 – Com 503 simulado em todas as chamadas, a resposta traz erro legível após 2 novas tentativas. | Critério de aceite | CT05 |
| RN01 – Sem '/' no nome: cliente Gemini nativo. | Regra de negócio do PBI | CT01 |
| RN02 – Com prefixo de provedor: LiteLLM. | Regra de negócio do PBI | CT01 |
| RN03 – O comportamento da v2 não muda. | Regra de negócio do PBI | CT04 |
| RN04 – Erro temporário do modelo (503/UNAVAILABLE) tem até 2 novas tentativas com espera crescente, com a mesma regra adotada na v2 após o teste do PR #5; erro 400 e erro de ferramenta não são repetidos. | Regra de negócio do PBI | CT05 |
| RN02 (F-V3.3) | Regra da feature/épico ou task | CT02 |
| RN03 | Regra da feature/épico ou task | CT04 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- Os nomes exatos das mensagens de log serão definidos na implementação; os cenários verificam o conteúdo, não o texto literal.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V4.1.1 Ambiente de homologação v4 publicado a partir do branch homolog-v4

Arquivo: `out/bdd/F-V4.1.1.feature` · 7 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O Space ds-fabiopinheiro/ap2-homolog-v4 fica em estado Running a partir do branch homolog-v4. | Critério de aceite | CT01 |
| CA2 – Um push de backend em homolog-v4 reconstrói apenas ds-fabiopinheiro/ap2-homolog-v4. | Critério de aceite | CT02 |
| CA3 – Após restart do Space da v4, o log mostra restore apenas de arquivos com environment='v4'. | Critério de aceite | CT04 |
| CA4 – A v2 (homolog-deploy) e as versões anteriores passam no roteiro de regressão depois da criação da nova versão. | Critério de aceite | CT05 |
| CA5 – Se o secret GOOGLE_API_KEY estiver ausente, o log de inicialização mostra o aviso e o agent card continua respondendo. | Critério de aceite | CT06 |
| RN01 – Todo trabalho da v4 entra por PR no branch homolog-v4; o branch homolog-v3 não recebe código da v4. | Regra de negócio do PBI | — |
| RN02 – O estado da v4 no Supabase fica separado das outras versões (AP2_ENV=v4). | Regra de negócio do PBI | CT04 |
| RN03 – Nenhum segredo é gravado no repositório, em variável VITE_* ou em variável pública do Space. | Regra de negócio do PBI | CT07 |
| RN do workflow (paths) | Regra da feature/épico ou task | CT03 |
| RN03 | Regra da feature/épico ou task | CT07 |

### Cenários

```gherkin
# language: pt
@v4 @F-V4.1.1
Funcionalidade: Ambiente de homologação v4 (homolog-v4)
  PBI F-V4.1.1 · Ambiente de homologação v4 publicado a partir do branch homolog-v4

  Contexto:
    Dado que o branch homolog-v4 foi criado a partir de homolog-v3

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Space da v4 publicado a partir do branch homolog-v4
    Dado que o Space ds-fabiopinheiro/ap2-homolog-v4 está configurado com AP2_REF=homolog-v4 e AP2_ENV=v4
    Quando o build do Space termina
    Então o estado exibido no Hugging Face é "Running"
    E GET https://ds-fabiopinheiro-ap2-homolog-v4.hf.space/a2a/shopping_agent/.well-known/agent-card.json retorna HTTP 200

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Push de backend em homolog-v4 reconstrói só o Space da v4
    Dado que os Spaces da v2 e da v4 estão em "Running"
    Quando um commit que altera deploy/hf-space/start.sh é enviado ao branch homolog-v4
    Então o workflow "HF Space rebuild" executa Factory rebuild de ds-fabiopinheiro/ap2-homolog-v4
    E o Space ds-fabiopinheiro/ap2-homolog-backend continua em "Running" sem rebuild

  @CT03 @negativo
  # Origem: RN do workflow (paths)
  Cenário: CT03 · Push só de documentação não dispara rebuild
    Dado que o Space da v4 está em "Running"
    Quando um commit que altera apenas CLAUDE.md é enviado ao branch homolog-v4
    Então o workflow "HF Space rebuild" não é executado

  @CT04 @positivo
  # Origem: CA3 / RN02
  Cenário: CT04 · Restore lê apenas o estado da v4
    Dado que ap2_env_state_files tem 3 arquivos com environment='v4' e 2 arquivos com environment='outra'
    Quando o Space da v4 é reiniciado
    Então o log de inicialização mostra "restored 3 file(s)"
    E nenhum arquivo de environment='outra' aparece em TEMP_DB_DIR

  @CT05 @regressao
  # Origem: CA4
  Cenário: CT05 · Compra autônoma da v2 continua funcionando após a criação da v4
    Dado que a v4 está publicada
    E o web client da v2 está aberto em https://ap2-homolog-frontend.vercel.app
    Quando o usuário aprova o mandate de um item com orçamento US$ 500 e o price drop é disparado com price=199 e stock=10
    Então a tela da v2 mostra "Compra concluída" com valor US$ 199,00
    E a tabela ap2_mandates da v2 recebe 4 novas linhas

  @CT06 @negativo
  # Origem: CA5
  Cenário: CT06 · Space inicia sem GOOGLE_API_KEY
    Dado que o Space da v4 não tem o secret GOOGLE_API_KEY
    Quando o Space inicia
    Então o log mostra "WARNING: GOOGLE_API_KEY is not set"
    E o agent card público retorna HTTP 200

  @CT07 @seguranca
  # Origem: RN03
  Cenário: CT07 · Nenhum segredo no branch da versão
    Dado o conteúdo do branch homolog-v4
    Quando a varredura de segredos (gitleaks) é executada em todo o histórico do branch
    Então nenhum segredo é encontrado
```

### Lacunas identificadas
- Não está definido o comportamento de um Space ≠ v2 iniciado sem AP2_ENV: hoje o sync usaria as tabelas da v2. Sugestão: o start.sh encerrar com erro quando AP2_REF ≠ homolog-deploy e AP2_ENV estiver vazio.

### Premissas
- Nome dos Spaces e URLs seguem o padrão ds-fabiopinheiro/ap2-homolog-vN.
- gitleaks disponível no CI ou na máquina de quem testa.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V4.2.1 Credentials Provider Agent lista as formas de pagamento da conta de demonstração

Arquivo: `out/bdd/F-V4.2.1.feature` · 4 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Uma requisição A2A interna retorna a lista de formas de pagamento da demo. | Critério de aceite | CT01 |
| CA2 – Com o agente parado, o Shopping Agent v1 informa que não foi possível obter as formas de pagamento. | Critério de aceite | CT02 |
| RN01 – Só a conta de demonstração é retornada. | Regra de negócio do PBI | — |
| RN01 (F-V4.2) | Regra da feature/épico ou task | CT03 |
| Task: espelhamento no Supabase | Regra da feature/épico ou task | CT04 |

### Cenários

```gherkin
# language: pt
@v4 @F-V4.2.1
Funcionalidade: Credentials Provider Agent lista as formas de pagamento da conta de demonstração
  PBI F-V4.2.1 · Credentials Provider Agent lista as formas de pagamento da conta de demonstração

  Contexto:
    Dado que o Space da v4 está em "Running"
    E a conta de demonstração de account_manager.py está carregada

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Lista de formas de pagamento da demo
    Quando o Shopping Agent v1 pede as formas de pagamento da conta de demonstração
    Então a lista contém "American Express ending in 4444"

  @CT02 @negativo
  # Origem: CA2
  Cenário: CT02 · Credentials Provider fora do ar
    Dado que o processo do Credentials Provider Agent está parado
    Quando o usuário chega à etapa de forma de pagamento no ADK Web
    Então a conversa informa que não foi possível obter as formas de pagamento

  @CT03 @seguranca
  # Origem: RN01 (F-V4.2)
  Cenário: CT03 · Credentials Provider não é acessível de fora
    Quando é feito GET https://ds-fabiopinheiro-ap2-homolog-v4.hf.space/a2a/credentials_provider/.well-known/agent-card.json
    Então a resposta é HTTP 404

  @CT04 @positivo
  # Origem: Task: espelhamento no Supabase
  Cenário: CT04 · Estado mantido após restart
    Dado que uma forma de pagamento foi usada em uma compra da v4
    Quando o Space da v4 é reiniciado
    Então o log mostra restore com environment='v4'
    E a próxima compra usa a mesma conta de demonstração
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- A conta de demonstração contém o cartão com alias "American Express ending in 4444" (account_manager.py). Os dados são fictícios do repositório e não devem ser trocados por dados reais.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V4.3.1 Spike: forma de publicar o ADK Web atrás do nginx

Arquivo: `out/bdd/F-V4.3.1.feature` · 2 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Documento de decisão com pelo menos 2 alternativas, riscos e a escolhida. | Critério de aceite | CT02 |
| CA2 – Prova de conceito da alternativa escolhida abrindo /dev-ui pelo Space. | Critério de aceite | CT01 |
| RN01 – Resultado registrado como decisão no CLAUDE.md, com alternativas avaliadas. | Regra de negócio do PBI | CT02 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Spike: os cenários verificam só a entrega da investigação. Os comportamentos definitivos estão em F-V4.3.2.

### Premissas
- O caminho /dev-ui é o padrão do ADK Web; o spike pode definir outro.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V4.3.2 Compra assistida ponta a ponta pelo ADK Web

Arquivo: `out/bdd/F-V4.3.2.feature` · 7 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Cenário: compra concluída — Dado o ADK Web aberto, Quando o usuário completa as etapas e informa 123, Então recebe o recibo. | Critério de aceite | CT01 |
| CA2 – Cenário: OTP incorreto — Quando o usuário informa 000, Então o pagamento não é concluído. | Critério de aceite | CT02 |
| CA3 – Cenário: desistência — Quando o usuário recusa o carrinho, Então nenhum Payment Mandate é criado. | Critério de aceite | CT03 |
| CA4 – Os mandates da compra concluída aparecem em ap2_env_mandates com environment='v4'. | Critério de aceite | CT04 |
| CA5 – Com um 503 simulado na primeira chamada do Shopping Agent v1 ao modelo, a conversa continua após a nova tentativa. | Critério de aceite | CT07 |
| RN01 – Cada etapa exige confirmação do usuário. | Regra de negócio do PBI | CT03 |
| RN02 – OTP de demonstração 123. | Regra de negócio do PBI | CT01, CT02 |
| RN03 – Os mandates da jornada são registrados com environment='v4'. | Regra de negócio do PBI | CT04 |
| Métrica do épico | Regra da feature/épico ou task | CT06 |
| RN01 (F-V4.3) | Regra da feature/épico ou task | CT05 |

### Cenários

```gherkin
# language: pt
@v4 @F-V4.3.2
Funcionalidade: Compra assistida ponta a ponta pelo ADK Web
  PBI F-V4.3.2 · Compra assistida ponta a ponta pelo ADK Web

  Contexto:
    Dado que o ADK Web da v4 está aberto com o agente shopping_agent selecionado
    E Merchant, Credentials Provider e Processor Agents estão em execução

  @CT01 @positivo
  # Origem: CA1 / RN02
  Cenário: CT01 · Compra assistida concluída
    Dado que o usuário pediu "I want to buy a coffee maker" e escolheu uma das opções
    E escolheu a forma de pagamento "American Express ending in 4444" e assinou o Payment Mandate
    Quando informa o OTP "123"
    Então a conversa mostra a confirmação da compra com o recibo

  @CT02 @negativo
  # Origem: CA2 / RN02
  Cenário: CT02 · OTP incorreto
    Dado que o usuário chegou ao desafio OTP
    Quando informa o OTP "000"
    Então o pagamento não é concluído
    E a conversa informa que o OTP é inválido

  @CT03 @negativo
  # Origem: CA3 / RN01
  Cenário: CT03 · Usuário recusa o carrinho
    Dado que o Merchant apresentou as opções de compra
    Quando o usuário responde que não quer nenhuma delas
    Então nenhum Payment Mandate é criado em ap2_env_mandates com environment='v4'

  @CT04 @positivo
  # Origem: CA4 / RN03
  Cenário: CT04 · Mandates da compra registrados
    Dado que o CT01 foi concluído às <hora_do_teste>
    Quando é consultado ap2_env_mandates com environment='v4' e first_seen_at posterior a <hora_do_teste>
    Então existe o Payment Mandate da compra

  @CT05 @seguranca
  # Origem: RN01 (F-V4.3)
  Cenário: CT05 · ADK Web lista só o Shopping Agent v1
    Quando o visitante abre o seletor de agentes do ADK Web
    Então a lista contém apenas "shopping_agent"

  @CT06 @performance
  # Origem: Métrica do épico
  Cenário: CT06 · Consumo do Gemini em uma compra assistida
    Dado que nenhum outro teste usa a GOOGLE_API_KEY no período
    Quando o CT01 é executado 1 vez
    Então o pico de RPM no AI Studio é menor que 15

  @CT07 @negativo
  # Origem: CA5
  Cenário: CT07 · Erro 503 temporário no Shopping Agent v1
    Dado que a primeira chamada do Shopping Agent v1 ao modelo retorna 503 (simulado em teste unitário)
    Quando o usuário envia "I want to buy a coffee maker"
    Então a conversa continua com as opções de compra após a nova tentativa
```

### Lacunas identificadas
- O limite de requisições do ADK Web depende da decisão do spike F-V4.3.1; o cenário será escrito depois dela.

### Premissas
- OTP de demonstração "123" conforme o README do cenário human-present.
- A conversa no ADK Web é em inglês até a tradução pt-BR alcançar o Shopping Agent v1.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V5.1.1 Ambiente de homologação v5 publicado a partir do branch homolog-v5

Arquivo: `out/bdd/F-V5.1.1.feature` · 8 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O Space ds-fabiopinheiro/ap2-homolog-v5 fica em estado Running a partir do branch homolog-v5. | Critério de aceite | CT01 |
| CA2 – Um push de backend em homolog-v5 reconstrói apenas ds-fabiopinheiro/ap2-homolog-v5. | Critério de aceite | CT02 |
| CA3 – A URL https://ap2-homolog-v5-frontend.vercel.app abre sem login. | Critério de aceite | CT08 |
| CA4 – Após restart do Space da v5, o log mostra restore apenas de arquivos com environment='v5'. | Critério de aceite | CT04 |
| CA5 – A v2 (homolog-deploy) e as versões anteriores passam no roteiro de regressão depois da criação da nova versão. | Critério de aceite | CT05 |
| CA6 – Se o secret GOOGLE_API_KEY estiver ausente, o log de inicialização mostra o aviso e o agent card continua respondendo. | Critério de aceite | CT06 |
| RN01 – Todo trabalho da v5 entra por PR no branch homolog-v5; o branch homolog-v4 não recebe código da v5. | Regra de negócio do PBI | — |
| RN02 – O estado da v5 no Supabase fica separado das outras versões (AP2_ENV=v5). | Regra de negócio do PBI | CT04 |
| RN03 – Nenhum segredo é gravado no repositório, em variável VITE_* ou em variável pública do Space. | Regra de negócio do PBI | CT07 |
| RN do workflow (paths) | Regra da feature/épico ou task | CT03 |
| RN03 | Regra da feature/épico ou task | CT07 |

### Cenários

```gherkin
# language: pt
@v5 @F-V5.1.1
Funcionalidade: Ambiente de homologação v5 (homolog-v5)
  PBI F-V5.1.1 · Ambiente de homologação v5 publicado a partir do branch homolog-v5

  Contexto:
    Dado que o branch homolog-v5 foi criado a partir de homolog-v4

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Space da v5 publicado a partir do branch homolog-v5
    Dado que o Space ds-fabiopinheiro/ap2-homolog-v5 está configurado com AP2_REF=homolog-v5 e AP2_ENV=v5
    Quando o build do Space termina
    Então o estado exibido no Hugging Face é "Running"
    E GET https://ds-fabiopinheiro-ap2-homolog-v5.hf.space/a2a/shopping_agent/.well-known/agent-card.json retorna HTTP 200

  @CT08 @positivo
  # Origem: CA3
  Cenário: CT08 · Frontend da v5 abre sem login
    Dado que o projeto Vercel ap2-homolog-v5-frontend tem produção no branch homolog-v5
    Quando um visitante sem conta no Vercel abre https://ap2-homolog-v5-frontend.vercel.app
    Então a página inicial do web client é exibida sem pedido de login

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Push de backend em homolog-v5 reconstrói só o Space da v5
    Dado que os Spaces da v2 e da v5 estão em "Running"
    Quando um commit que altera deploy/hf-space/start.sh é enviado ao branch homolog-v5
    Então o workflow "HF Space rebuild" executa Factory rebuild de ds-fabiopinheiro/ap2-homolog-v5
    E o Space ds-fabiopinheiro/ap2-homolog-backend continua em "Running" sem rebuild

  @CT03 @negativo
  # Origem: RN do workflow (paths)
  Cenário: CT03 · Push só de documentação não dispara rebuild
    Dado que o Space da v5 está em "Running"
    Quando um commit que altera apenas CLAUDE.md é enviado ao branch homolog-v5
    Então o workflow "HF Space rebuild" não é executado

  @CT04 @positivo
  # Origem: CA4 / RN02
  Cenário: CT04 · Restore lê apenas o estado da v5
    Dado que ap2_env_state_files tem 3 arquivos com environment='v5' e 2 arquivos com environment='outra'
    Quando o Space da v5 é reiniciado
    Então o log de inicialização mostra "restored 3 file(s)"
    E nenhum arquivo de environment='outra' aparece em TEMP_DB_DIR

  @CT05 @regressao
  # Origem: CA5
  Cenário: CT05 · Compra autônoma da v2 continua funcionando após a criação da v5
    Dado que a v5 está publicada
    E o web client da v2 está aberto em https://ap2-homolog-frontend.vercel.app
    Quando o usuário aprova o mandate de um item com orçamento US$ 500 e o price drop é disparado com price=199 e stock=10
    Então a tela da v2 mostra "Compra concluída" com valor US$ 199,00
    E a tabela ap2_mandates da v2 recebe 4 novas linhas

  @CT06 @negativo
  # Origem: CA6
  Cenário: CT06 · Space inicia sem GOOGLE_API_KEY
    Dado que o Space da v5 não tem o secret GOOGLE_API_KEY
    Quando o Space inicia
    Então o log mostra "WARNING: GOOGLE_API_KEY is not set"
    E o agent card público retorna HTTP 200

  @CT07 @seguranca
  # Origem: RN03
  Cenário: CT07 · Nenhum segredo no branch da versão
    Dado o conteúdo do branch homolog-v5
    Quando a varredura de segredos (gitleaks) é executada em todo o histórico do branch
    Então nenhum segredo é encontrado
```

### Lacunas identificadas
- Não está definido o comportamento de um Space ≠ v2 iniciado sem AP2_ENV: hoje o sync usaria as tabelas da v2. Sugestão: o start.sh encerrar com erro quando AP2_REF ≠ homolog-deploy e AP2_ENV estiver vazio.

### Premissas
- Nome dos Spaces e URLs seguem o padrão ds-fabiopinheiro/ap2-homolog-vN.
- gitleaks disponível no CI ou na máquina de quem testa.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V5.2.1 Spike: protocolo entre web client e Shopping Agent v1

Arquivo: `out/bdd/F-V5.2.1.feature` · 2 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Documento com o contrato dos artifacts (tipos e campos) de cada etapa da jornada assistida. | Critério de aceite | CT01 |
| CA2 – Prova de conceito recebendo o primeiro artifact no web client. | Critério de aceite | CT02 |
| RN01 – Decisão registrada no CLAUDE.md. | Regra de negócio do PBI | CT01 |

### Cenários

```gherkin
# language: pt
@v5 @F-V5.2.1
Funcionalidade: Spike: protocolo entre web client e Shopping Agent v1
  PBI F-V5.2.1 · Spike: protocolo entre web client e Shopping Agent v1

  Contexto:
    Dado que a prova de conceito está publicada na v5

  @CT01 @positivo
  # Origem: CA1 / RN01
  Cenário: CT01 · Contrato de artifacts documentado
    Quando o CLAUDE.md do branch homolog-v5 é revisado
    Então há o contrato (tipos e campos) dos artifacts de cada etapa da jornada assistida

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Primeiro artifact recebido pela tela
    Dado que https://ap2-homolog-v5-frontend.vercel.app está configurado para o Shopping Agent v1
    Quando o usuário envia a primeira mensagem na prova de conceito
    Então a tela recebe um artifact do tipo definido no contrato
```

### Lacunas identificadas
- Spike: os comportamentos finais estão em F-V5.2.2 e F-V5.3.x.

### Premissas
- Nenhuma.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V5.2.2 Escolha entre jornada autônoma e assistida na tela inicial

Arquivo: `out/bdd/F-V5.2.2.feature` · 7 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – A tela inicial mostra as duas opções com uma descrição curta de cada. | Critério de aceite | CT01 |
| CA2 – Ao escolher a assistida, as mensagens vão para o Shopping Agent v1. | Critério de aceite | CT02 |
| CA3 – Ao trocar de jornada no meio da conversa, a tela pede confirmação e inicia nova sessão. | Critério de aceite | CT03, CT04 |
| RN01 – A escolha fica visível durante toda a conversa. | Regra de negócio do PBI | CT05 |
| RN02 – Trocar de jornada inicia nova conversa. | Regra de negócio do PBI | CT03, CT04 |
| CA (F-V5.2) | Regra da feature/épico ou task | CT06 |
| RN01 | Regra da feature/épico ou task | CT05 |
| RN01 (F-V5.2) | Regra da feature/épico ou task | CT07 |

### Cenários

```gherkin
# language: pt
@v5 @F-V5.2.2
Funcionalidade: Escolha entre jornada autônoma e assistida
  PBI F-V5.2.2 · Escolha entre jornada autônoma e assistida na tela inicial

  Contexto:
    Dado que o usuário abre https://ap2-homolog-v5-frontend.vercel.app

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Tela inicial com as duas jornadas
    Quando a página termina de carregar
    Então a tela mostra as opções "Compra autônoma" e "Compra assistida" com uma descrição curta de cada

  @CT02 @positivo
  # Origem: CA2 / RN02 (F-V5.2)
  Cenário: CT02 · Jornada assistida usa o Shopping Agent v1
    Dado que o usuário escolheu "Compra assistida"
    Quando envia a mensagem "I want to buy a coffee maker"
    Então a requisição A2A é enviada para a URL de VITE_ASSISTED_AGENT_URL

  @CT03 @positivo
  # Origem: CA3 / RN02
  Cenário: CT03 · Troca de jornada pede confirmação
    Dado que o usuário está numa conversa da "Compra assistida"
    Quando escolhe "Compra autônoma"
    Então a tela pede confirmação para iniciar nova conversa

  @CT04 @positivo
  # Origem: CA3 / RN02
  Cenário: CT04 · Troca confirmada inicia nova sessão
    Dado que a tela pediu confirmação de troca de jornada
    Quando o usuário confirma
    Então a conversa anterior some da tela
    E a próxima mensagem é enviada com um sessionId diferente do anterior

  @CT05 @negativo
  # Origem: RN01
  Cenário: CT05 · Troca cancelada mantém a conversa
    Dado que a tela pediu confirmação de troca de jornada
    Quando o usuário cancela
    Então a conversa atual continua exibida na mesma jornada

  @CT06 @negativo
  # Origem: CA (F-V5.2)
  Cenário: CT06 · Agente da jornada assistida fora do ar
    Dado que o Shopping Agent v1 da v5 não responde
    Quando o usuário envia uma mensagem na "Compra assistida"
    Então a tela mostra uma mensagem iniciada por "Erro de conexão"
    E a opção "Compra autônoma" continua disponível

  @CT07 @regressao
  # Origem: RN01 (F-V5.2)
  Cenário: CT07 · Compra autônoma no web client da v5
    Dado que o usuário escolheu "Compra autônoma"
    Quando executa o roteiro de compra autônoma com price drop price=199 e stock=10
    Então a tela mostra "Compra concluída" com valor US$ 199,00
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- Os rótulos "Compra autônoma" e "Compra assistida" são sugestão; o texto final segue a tradução pt-BR.
- Textos da jornada autônoma conforme o PR #5 ("Compra concluída", "Erro de conexão"), validados no teste de aceitação de 27/09/2026.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V5.3.1 Seleção das opções de compra do Merchant

Arquivo: `out/bdd/F-V5.3.1.feature` · 5 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – A tela lista as opções recebidas com nome, preço e comerciante. | Critério de aceite | CT01 |
| CA2 – Ao escolher uma opção, a escolha é enviada ao agente e a próxima etapa aparece. | Critério de aceite | CT02 |
| CA3 – Sem opções retornadas, a tela mostra mensagem e permite refazer o pedido. | Critério de aceite | CT03 |
| RN01 – A tela mostra nome, preço e comerciante de cada opção. | Regra de negócio do PBI | CT01 |
| RN02 – Só uma opção pode ser escolhida. | Regra de negócio do PBI | CT04 |
| RN02 | Regra da feature/épico ou task | CT04 |
| RN03 (F-V5.3) | Regra da feature/épico ou task | CT05 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- O Merchant devolve 3 opções no CT01; o número real depende do catálogo gerado pelo sample.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V5.3.2 Escolha da forma de pagamento e assinatura do Payment Mandate na Trusted Surface

Arquivo: `out/bdd/F-V5.3.2.feature` · 6 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – A tela lista as formas de pagamento da conta de demonstração. | Critério de aceite | CT01 |
| CA2 – A Trusted Surface mostra item, valor, comerciante e forma de pagamento. | Critério de aceite | CT02 |
| CA3 – Ao recusar, a compra é encerrada e nenhum Payment Mandate é criado. | Critério de aceite | CT03 |
| CA4 – Ao assinar, o Payment Mandate aparece na aba Mandates. | Critério de aceite | CT04 |
| RN01 – A Trusted Surface mostra item, valor, comerciante e forma de pagamento antes de assinar. | Regra de negócio do PBI | CT02, CT05 |
| RN02 – Sem assinatura, nenhum pagamento é iniciado. | Regra de negócio do PBI | CT03, CT06 |
| RN01 | Regra da feature/épico ou task | CT05 |
| RN02 | Regra da feature/épico ou task | CT06 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- O valor no Payment Mandate segue a convenção de centavos da v2 (amount_range em centavos); confirmar no contrato do spike F-V5.2.1.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V5.3.3 Desafio OTP e recibo da compra assistida

Arquivo: `out/bdd/F-V5.3.3.feature` · 4 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Com OTP 123, a tela mostra o recibo com número do pedido, valor e forma de pagamento. | Critério de aceite | CT01 |
| CA2 – Com OTP errado, a tela mostra erro e permite nova tentativa. | Critério de aceite | CT02 |
| CA3 – (Se RN02 for confirmada) Após 3 OTPs errados, a compra é encerrada sem cobrança. | Critério de aceite | CT04 |
| RN01 – O campo OTP aceita só dígitos. | Regra de negócio do PBI | CT03 |
| RN02 – (Proposta, não vem do repositório; confirmar com o PO) Após 3 OTPs errados, a compra é encerrada. | Regra de negócio do PBI | — |
| RN01 | Regra da feature/épico ou task | CT03 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- CT04 depende da confirmação da RN02 (limite de 3 tentativas), que é proposta e não vem do repositório. Está marcado com @pendente-confirmacao.

### Premissas
- OTP de demonstração "123".

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V6.1.1 Ambiente de homologação v6 publicado a partir do branch homolog-v6

Arquivo: `out/bdd/F-V6.1.1.feature` · 7 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O Space ds-fabiopinheiro/ap2-homolog-v6 fica em estado Running a partir do branch homolog-v6. | Critério de aceite | CT01 |
| CA2 – Um push de backend em homolog-v6 reconstrói apenas ds-fabiopinheiro/ap2-homolog-v6. | Critério de aceite | CT02 |
| CA3 – Após restart do Space da v6, o log mostra restore apenas de arquivos com environment='v6'. | Critério de aceite | CT04 |
| CA4 – A v2 (homolog-deploy) e as versões anteriores passam no roteiro de regressão depois da criação da nova versão. | Critério de aceite | CT05 |
| CA5 – Se o secret GOOGLE_API_KEY estiver ausente, o log de inicialização mostra o aviso e o agent card continua respondendo. | Critério de aceite | CT06 |
| RN01 – Todo trabalho da v6 entra por PR no branch homolog-v6; o branch homolog-v5 não recebe código da v6. | Regra de negócio do PBI | — |
| RN02 – O estado da v6 no Supabase fica separado das outras versões (AP2_ENV=v6). | Regra de negócio do PBI | CT04 |
| RN03 – Nenhum segredo é gravado no repositório, em variável VITE_* ou em variável pública do Space. | Regra de negócio do PBI | CT07 |
| RN do workflow (paths) | Regra da feature/épico ou task | CT03 |
| RN03 | Regra da feature/épico ou task | CT07 |

### Cenários

```gherkin
# language: pt
@v6 @F-V6.1.1
Funcionalidade: Ambiente de homologação v6 (homolog-v6)
  PBI F-V6.1.1 · Ambiente de homologação v6 publicado a partir do branch homolog-v6

  Contexto:
    Dado que o branch homolog-v6 foi criado a partir de homolog-v5

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Space da v6 publicado a partir do branch homolog-v6
    Dado que o Space ds-fabiopinheiro/ap2-homolog-v6 está configurado com AP2_REF=homolog-v6 e AP2_ENV=v6
    Quando o build do Space termina
    Então o estado exibido no Hugging Face é "Running"
    E GET https://ds-fabiopinheiro-ap2-homolog-v6.hf.space/a2a/shopping_agent/.well-known/agent-card.json retorna HTTP 200

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Push de backend em homolog-v6 reconstrói só o Space da v6
    Dado que os Spaces da v2 e da v6 estão em "Running"
    Quando um commit que altera deploy/hf-space/start.sh é enviado ao branch homolog-v6
    Então o workflow "HF Space rebuild" executa Factory rebuild de ds-fabiopinheiro/ap2-homolog-v6
    E o Space ds-fabiopinheiro/ap2-homolog-backend continua em "Running" sem rebuild

  @CT03 @negativo
  # Origem: RN do workflow (paths)
  Cenário: CT03 · Push só de documentação não dispara rebuild
    Dado que o Space da v6 está em "Running"
    Quando um commit que altera apenas CLAUDE.md é enviado ao branch homolog-v6
    Então o workflow "HF Space rebuild" não é executado

  @CT04 @positivo
  # Origem: CA3 / RN02
  Cenário: CT04 · Restore lê apenas o estado da v6
    Dado que ap2_env_state_files tem 3 arquivos com environment='v6' e 2 arquivos com environment='outra'
    Quando o Space da v6 é reiniciado
    Então o log de inicialização mostra "restored 3 file(s)"
    E nenhum arquivo de environment='outra' aparece em TEMP_DB_DIR

  @CT05 @regressao
  # Origem: CA4
  Cenário: CT05 · Compra autônoma da v2 continua funcionando após a criação da v6
    Dado que a v6 está publicada
    E o web client da v2 está aberto em https://ap2-homolog-frontend.vercel.app
    Quando o usuário aprova o mandate de um item com orçamento US$ 500 e o price drop é disparado com price=199 e stock=10
    Então a tela da v2 mostra "Compra concluída" com valor US$ 199,00
    E a tabela ap2_mandates da v2 recebe 4 novas linhas

  @CT06 @negativo
  # Origem: CA5
  Cenário: CT06 · Space inicia sem GOOGLE_API_KEY
    Dado que o Space da v6 não tem o secret GOOGLE_API_KEY
    Quando o Space inicia
    Então o log mostra "WARNING: GOOGLE_API_KEY is not set"
    E o agent card público retorna HTTP 200

  @CT07 @seguranca
  # Origem: RN03
  Cenário: CT07 · Nenhum segredo no branch da versão
    Dado o conteúdo do branch homolog-v6
    Quando a varredura de segredos (gitleaks) é executada em todo o histórico do branch
    Então nenhum segredo é encontrado
```

### Lacunas identificadas
- Não está definido o comportamento de um Space ≠ v2 iniciado sem AP2_ENV: hoje o sync usaria as tabelas da v2. Sugestão: o start.sh encerrar com erro quando AP2_REF ≠ homolog-deploy e AP2_ENV estiver vazio.

### Premissas
- Nome dos Spaces e URLs seguem o padrão ds-fabiopinheiro/ap2-homolog-vN.
- gitleaks disponível no CI ou na máquina de quem testa.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V6.2.1 Binários Go no container com seleção de backend

Arquivo: `out/bdd/F-V6.2.1.feature` · 3 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – O build do Space conclui com os binários Go. | Critério de aceite | CT01 |
| CA2 – Com AP2_BACKEND_LANG=go, o log mostra os agentes Go iniciados. | Critério de aceite | CT02 |
| CA3 – Com valor inválido, o container usa python e registra aviso. | Critério de aceite | CT02, CT03 |
| RN01 – Build Go em estágio separado do Dockerfile; imagem final só com os binários. | Regra de negócio do PBI | CT01 |

### Cenários

```gherkin
# language: pt
@v6 @F-V6.2.1
Funcionalidade: Binários Go no container com seleção de backend
  PBI F-V6.2.1 · Binários Go no container com seleção de backend

  Contexto:
    Dado que o Dockerfile da v6 tem o estágio de build Go

  @CT01 @positivo
  # Origem: CA1 / RN01
  Cenário: CT01 · Build do Space com os binários Go
    Quando o build do Space da v6 termina
    Então o estado do Space é "Running"
    E os binários Go estão presentes na imagem final

  @CT02 @positivo
  # Origem: CA2 / CA3 / RN01 (F-V6.2)
  Esquema do Cenário: CT02 · Seleção do backend por variável
    Dado que AP2_BACKEND_LANG é <valor>
    Quando o Space inicia
    Então o log mostra os agentes de 8001–8003 iniciados em <linguagem>

    Exemplos:
      | valor     | linguagem |
      | python    | Python    |
      | go        | Go        |
      | (ausente) | Python    |

  @CT03 @negativo
  # Origem: CA3
  Cenário: CT03 · Valor inválido volta para Python com aviso
    Dado que AP2_BACKEND_LANG é "rust"
    Quando o Space inicia
    Então o log mostra aviso de valor inválido
    E os agentes de 8001–8003 são iniciados em Python
```

### Lacunas identificadas
- Nenhuma.

### Premissas
- O aviso de valor inválido é texto livre no log; o cenário verifica a existência do aviso.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V6.2.2 Compra assistida com backend Go

Arquivo: `out/bdd/F-V6.2.2.feature` · 3 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Compra concluída com OTP 123 e recibo. | Critério de aceite | CT01 |
| CA2 – Mandates registrados com environment='v6'. | Critério de aceite | CT02 |
| RN01 – Mesmo roteiro da v4/v5. | Regra de negócio do PBI | — |
| RN01 (mesmo roteiro da v4/v5) | Regra da feature/épico ou task | CT03 |

### Cenários

```gherkin
# language: pt
@v6 @F-V6.2.2
Funcionalidade: Compra assistida com backend Go
  PBI F-V6.2.2 · Compra assistida com backend Go

  Contexto:
    Dado que o Space da v6 está com AP2_BACKEND_LANG=go
    E o usuário está na "Compra assistida" do web client apontado para a v6

  @CT01 @positivo
  # Origem: CA1
  Cenário: CT01 · Compra concluída com backend Go
    Dado que o usuário escolheu uma opção e "American Express ending in 4444" e assinou o Payment Mandate
    Quando informa o OTP "123"
    Então a tela mostra o recibo da compra

  @CT02 @positivo
  # Origem: CA2
  Cenário: CT02 · Mandates registrados na v6
    Dado que o CT01 foi concluído às <hora_do_teste>
    Quando é consultado ap2_env_mandates com environment='v6' e first_seen_at posterior a <hora_do_teste>
    Então existe o Payment Mandate da compra

  @CT03 @negativo
  # Origem: RN01 (mesmo roteiro da v4/v5)
  Cenário: CT03 · OTP errado com backend Go
    Quando o usuário informa o OTP "000"
    Então o pagamento não é concluído
```

### Lacunas identificadas
- Se os agentes Go gravarem estado fora de TEMP_DB_DIR, o CT02 precisa de ajuste (premissa do épico).

### Premissas
- Os agentes Go usam a mesma conta de demonstração e o mesmo OTP 123 dos agentes Python; confirmar no código Go.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V6.3.1 App Android configurado para o backend público sem chave no APK

Arquivo: `out/bdd/F-V6.3.1.feature` · 5 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Com o APK instalado, o app se conecta ao Space da v6 por HTTPS. | Critério de aceite | CT01 |
| CA2 – O APK não contém a chave do Gemini. | Critério de aceite | CT02 |
| CA3 – Com o backend fora do ar, o app mostra erro de conexão. | Critério de aceite | CT03 |
| RN01 – URLs do Merchant e do Credentials Provider vêm do build (gradle) ou da tela de configurações. | Regra de negócio do PBI | CT01 |
| RN02 – As chamadas ao Gemini passam por um endpoint do backend com limite de requisições. | Regra de negócio do PBI | CT05 |
| RN02 | Regra da feature/épico ou task | CT05 |
| RN02 (F-V6.3) | Regra da feature/épico ou task | CT04 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- O limite do proxy do Gemini (CT05) não está definido; <limite> precisa ser decidido antes do teste.

### Premissas
- O prefixo "AIza" é o formato atual das chaves de API do Google; ajustar a busca se o formato mudar.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.

## Preview — Cenários de teste · PBI F-V6.3.2 APK de homologação publicado no GitHub Releases

Arquivo: `out/bdd/F-V6.3.2.feature` · 4 cenários

### Matriz de cobertura

| Regra / critério | Origem | Cenários |
|---|---|---|
| CA1 – Um push de tag v6.* gera o APK no GitHub Releases. | Critério de aceite | CT01 |
| CA2 – O APK instala em aparelho físico e abre a tela inicial. | Critério de aceite | CT03 |
| CA3 – Uma compra com DPC é concluída em aparelho físico compatível. | Critério de aceite | CT04 |
| RN01 – Cada release v6.x publica um APK com o número da versão. | Regra de negócio do PBI | CT01, CT02 |
| RN02 – O workflow não usa segredos além dos necessários para assinar o APK de homologação. | Regra de negócio do PBI | — |
| RN01 | Regra da feature/épico ou task | CT02 |

### Cenários

```gherkin
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
```

### Lacunas identificadas
- Os requisitos de aparelho para DPC não estão documentados no repositório; o CT04 depende de um aparelho validado previamente.

### Premissas
- minSdk 26 lido de android/shopping_assistant/app/build.gradle.kts.

### Pendências para sincronizar
- Onde os cenários ficam no GitHub: seção "Cenários de teste (BDD)" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.
- Massa de teste e acesso aos Spaces/Supabase da versão.
