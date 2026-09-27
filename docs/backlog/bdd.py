# -*- coding: utf-8 -*-
"""Cenários BDD (Gherkin pt-BR) dos 20 PBIs do backlog v3–v6.

Cada cenário: (id, tipo, nome, passos, origem). Tipos: positivo, negativo, borda,
seguranca, performance, regressao. Passos: lista de strings já com a palavra-chave.
"""

BASE = "https://ds-fabiopinheiro-ap2-homolog-{v}.hf.space"


def env_bdd(v, prev, vercel=False):
    base = BASE.format(v=v)
    space = f"ds-fabiopinheiro/ap2-homolog-{v}"
    sc = [
        ("CT01", "positivo", f"Space da {v} publicado a partir do branch homolog-{v}", [
            f"Dado que o Space {space} está configurado com AP2_REF=homolog-{v} e AP2_ENV={v}",
            "Quando o build do Space termina",
            'Então o estado exibido no Hugging Face é "Running"',
            f'E GET {base}/a2a/shopping_agent/.well-known/agent-card.json retorna HTTP 200'], "CA1"),
        ("CT02", "positivo", f"Push de backend em homolog-{v} reconstrói só o Space da {v}", [
            f"Dado que os Spaces da v2 e da {v} estão em \"Running\"",
            f"Quando um commit que altera deploy/hf-space/start.sh é enviado ao branch homolog-{v}",
            f"Então o workflow \"HF Space rebuild\" executa Factory rebuild de {space}",
            "E o Space ds-fabiopinheiro/ap2-homolog-backend continua em \"Running\" sem rebuild"], "CA2"),
        ("CT03", "negativo", "Push só de documentação não dispara rebuild", [
            f"Dado que o Space da {v} está em \"Running\"",
            f"Quando um commit que altera apenas CLAUDE.md é enviado ao branch homolog-{v}",
            "Então o workflow \"HF Space rebuild\" não é executado"], "RN do workflow (paths)"),
        ("CT04", "positivo", f"Restore lê apenas o estado da {v}", [
            f"Dado que ap2_env_state_files tem 3 arquivos com environment='{v}' e 2 arquivos com environment='outra'",
            f"Quando o Space da {v} é reiniciado",
            'Então o log de inicialização mostra "restored 3 file(s)"',
            "E nenhum arquivo de environment='outra' aparece em TEMP_DB_DIR"], "CA3 / RN02"),
        ("CT05", "regressao", f"Compra autônoma da v2 continua funcionando após a criação da {v}", [
            f"Dado que a {v} está publicada",
            "E o web client da v2 está aberto em https://ap2-homolog-frontend.vercel.app",
            "Quando o usuário aprova o mandate de um item com orçamento US$ 500 e o price drop é disparado com price=199 e stock=10",
            'Então a tela da v2 mostra "Compra concluída" com valor US$ 199,00',
            "E a tabela ap2_mandates da v2 recebe 4 novas linhas"], "CA4"),
        ("CT06", "negativo", "Space inicia sem GOOGLE_API_KEY", [
            f"Dado que o Space da {v} não tem o secret GOOGLE_API_KEY",
            "Quando o Space inicia",
            'Então o log mostra "WARNING: GOOGLE_API_KEY is not set"',
            "E o agent card público retorna HTTP 200"], "CA5"),
        ("CT07", "seguranca", "Nenhum segredo no branch da versão", [
            f"Dado o conteúdo do branch homolog-{v}",
            "Quando a varredura de segredos (gitleaks) é executada em todo o histórico do branch",
            "Então nenhum segredo é encontrado"], "RN03"),
    ]
    if vercel:
        remap = {"CA3 / RN02": "CA4 / RN02", "CA4": "CA5", "CA5": "CA6"}
        sc = [(a, b, c, d, remap.get(e, e)) for (a, b, c, d, e) in sc]
        sc.insert(1, ("CT08", "positivo", f"Frontend da {v} abre sem login", [
            f"Dado que o projeto Vercel ap2-homolog-{v}-frontend tem produção no branch homolog-{v}",
            f"Quando um visitante sem conta no Vercel abre https://ap2-homolog-{v}-frontend.vercel.app",
            "Então a página inicial do web client é exibida sem pedido de login"], "CA3"))
    return dict(
        feature=f"Ambiente de homologação {v} (homolog-{v})",
        contexto=[f"Dado que o branch homolog-{v} foi criado a partir de {prev}"],
        cenarios=sc,
        lacunas=[f"Não está definido o comportamento de um Space ≠ v2 iniciado sem AP2_ENV: hoje o sync usaria as tabelas da v2. Sugestão: o start.sh encerrar com erro quando AP2_REF ≠ homolog-deploy e AP2_ENV estiver vazio."],
        premissas=["Nome dos Spaces e URLs seguem o padrão ds-fabiopinheiro/ap2-homolog-vN.", "gitleaks disponível no CI ou na máquina de quem testa."])


BDD = {}
BDD["F-V3.1.1"] = env_bdd("v3", "homolog-deploy")
BDD["F-V4.1.1"] = env_bdd("v4", "homolog-v3")
BDD["F-V5.1.1"] = env_bdd("v5", "homolog-v4", vercel=True)
BDD["F-V6.1.1"] = env_bdd("v6", "homolog-v5")

B3 = BASE.format(v="v3")

BDD["F-V3.2.1"] = dict(
    feature="Merchant Agent acessível por A2A com agent card público",
    contexto=[f"Dado que o Space da v3 está em \"Running\" em {B3}"],
    cenarios=[
        ("CT01", "positivo", "Agent card público do Merchant Agent", [
            f"Quando é feito GET {B3}/a2a/merchant_agent/.well-known/agent-card.json",
            "Então a resposta é HTTP 200 com Content-Type application/json"], "CA1"),
        ("CT02", "positivo", "URL do agent card aponta para o Space", [
            "Quando o agent card do Merchant Agent é consultado",
            f'Então o campo "url" é "{B3}/a2a/merchant_agent"'], "CA1 / RN01"),
        ("CT03", "negativo", "Queda do Merchant Agent reinicia o container", [
            "Dado que o processo do Merchant Agent é encerrado dentro do container",
            "Quando o Hugging Face reinicia o Space",
            "Então o agent card do Merchant Agent volta a retornar HTTP 200"], "CA2"),
        ("CT04", "borda", "Limite de requisições por visitante", [
            "Dado que o limite da rota é 20 requisições/min com rajada de 10",
            "Quando o mesmo visitante envia <total> requisições simultâneas ao agent card",
            "Então <aceitas> respostas têm HTTP 200",
            "E <recusadas> respostas têm HTTP 429"], "CA3 / RN02",
         [("total", "aceitas", "recusadas"), ("11", "11", "0"), ("12", "11", "1"), ("15", "11", "4")]),
        ("CT05", "seguranca", "Resposta 429 legível pelo navegador", [
            "Dado que o visitante já excedeu o limite da rota /a2a/merchant_agent",
            "Quando envia mais uma requisição com Origin https://ap2-homolog-v5-frontend.vercel.app",
            'Então o corpo da resposta 429 contém "rate_limited"',
            'E o cabeçalho Access-Control-Allow-Origin é "*"'], "CA3"),
        ("CT06", "regressao", "Shopping Agent v2 continua no Space da v3", [
            f"Quando é feito GET {B3}/a2a/shopping_agent/.well-known/agent-card.json",
            "Então a resposta é HTTP 200"], "CA4"),
    ],
    lacunas=[],
    premissas=["O Space da v3 herda do nginx da v2 os valores de limite (20/min por visitante, rajada 10, nodelay).",
               "O visitante é identificado pelo último IP do X-Forwarded-For, como na v2."])

BDD["F-V3.2.2"] = dict(
    feature="Busca de produto no Merchant Agent com resposta assinada",
    contexto=["Dado que o Merchant Agent da v3 está publicado",
              "E o script deploy/tests/merchant_a2a_test.py está configurado com a URL do Space da v3"],
    cenarios=[
        ("CT01", "positivo", "Pedido de produto retorna opções assinadas", [
            'Quando o script envia a intenção de compra "coffee maker" com a extensão AP2',
            "Então a resposta contém pelo menos 1 opção de compra",
            "E cada opção contém uma assinatura do Merchant"], "CA1"),
        ("CT02", "positivo", "Assinatura válida é aceita pelo script", [
            "Dado uma resposta recebida do Merchant Agent",
            "Quando o script verifica a assinatura com a chave pública do Merchant",
            'Então o script imprime "OK" e termina com código 0'], "CA2 / RN02"),
        ("CT03", "negativo", "Assinatura alterada é recusada pelo script", [
            "Dado uma resposta recebida do Merchant Agent com 1 byte da assinatura alterado",
            "Quando o script verifica a assinatura",
            'Então o script imprime "FALHA" e termina com código diferente de 0'], "CA3 / RN02"),
        ("CT04", "positivo", "Mandates registrados no Supabase da v3", [
            "Dado que o CT01 foi executado às <hora_do_teste>",
            "Quando é consultado ap2_env_mandates com environment='v3' e first_seen_at posterior a <hora_do_teste>",
            "Então existe pelo menos 1 linha"], "CA4"),
        ("CT05", "negativo", "Mensagem sem a extensão AP2", [
            'Quando o script envia a intenção "coffee maker" sem declarar a extensão AP2 (EXTENSION_URI)',
            "Então o Merchant Agent responde com erro e não devolve opção assinada"], "RN01"),
        ("CT06", "performance", "Consumo do Gemini em 3 execuções seguidas", [
            "Dado que nenhum outro teste usa a GOOGLE_API_KEY no período",
            "Quando o CT01 é executado 3 vezes seguidas",
            "Então o pico de RPM no AI Studio para gemini-3.1-flash-lite-preview é menor que 15"], "Métrica do épico"),
    ],
    lacunas=["Comportamento para produto que o Merchant não conhece não está definido no repositório; não há cenário."],
    premissas=["O retorno de erro no CT05 depende de o Merchant exigir a extensão AP2 (required_extensions em remote_agents.py sugere que sim); confirmar.",
               "\"coffee maker\" é o exemplo do README do cenário human-present."])

BDD["F-V3.3.1"] = dict(
    feature="Merchant Payment Processor Agent em execução interna",
    contexto=["Dado que o Space da v3 está em \"Running\""],
    cenarios=[
        ("CT01", "positivo", "Processor responde dentro do container", [
            "Quando é feito GET http://127.0.0.1:8003/a2a/merchant_payment_processor_agent/.well-known/agent-card.json dentro do container",
            "Então a resposta é HTTP 200"], "CA1 / RN01"),
        ("CT02", "seguranca", "Processor não é acessível de fora", [
            f"Quando é feito GET {B3}/a2a/merchant_payment_processor_agent/.well-known/agent-card.json",
            "Então a resposta é HTTP 404"], "CA2 / RN01"),
        ("CT03", "negativo", "Queda do Processor reinicia o container", [
            "Dado que o processo do Processor Agent é encerrado",
            "Quando o Hugging Face reinicia o Space",
            "Então o agent card local do Processor volta a retornar HTTP 200"], "CA3"),
    ],
    lacunas=["O desafio OTP (RN02) só pode ser exercitado com o Shopping Agent v1; está coberto em F-V4.3.2 (CT01 e CT02)."],
    premissas=["O teste interno (CT01) é feito pelo terminal do Space (Dev Mode) ou por log de health check."])

BDD["F-V3.3.2"] = dict(
    feature="Modelo dos agentes A2A definido por AGENT_MODEL",
    contexto=["Dado que o Space da v3 tem GOOGLE_API_KEY e VERCEL_AI_GATEWAY_API_KEY cadastrados"],
    cenarios=[
        ("CT01", "positivo", "Cliente usado conforme o nome do modelo", [
            "Dado que AGENT_MODEL é <modelo>",
            "Quando o Space inicia e o script de F-V3.2.2 (CT01) é executado",
            "Então o log dos agentes A2A mostra o cliente <cliente>",
            'E o script imprime "OK"'], "CA1 / CA2 / RN01 / RN02",
         [("modelo", "cliente"), ("gemini-3.1-flash-lite-preview", "Gemini nativo"),
          ("vercel_ai_gateway/google/gemini-3.1-flash-lite-preview", "LiteLLM")]),
        ("CT02", "borda", "AGENT_MODEL ausente usa o padrão", [
            "Dado que a variável AGENT_MODEL não existe no Space",
            "Quando o Space inicia",
            'Então o log dos agentes A2A mostra o modelo "gemini-3.1-flash-lite-preview"'], "RN02 (F-V3.3)"),
        ("CT03", "negativo", "Modelo inválido", [
            'Dado que AGENT_MODEL é "modelo-inexistente"',
            "Quando o script de F-V3.2.2 é executado",
            "Então o log dos agentes A2A mostra erro de modelo não encontrado",
            "E o agent card do Merchant Agent continua retornando HTTP 200"], "CA3"),
        ("CT04", "regressao", "Troca de modelo na v3 não altera a v2", [
            'Dado que AGENT_MODEL da v3 é "vercel_ai_gateway/google/gemini-3.1-flash-lite-preview"',
            "Quando a compra autônoma da v2 é executada",
            "Então a compra é concluída",
            'E o log da v2 mostra "AGENT_MODEL=gemini-3.1-flash-lite-preview"'], "RN03"),
        ("CT05", "negativo", "Nova tentativa em erro temporário do modelo", [
            "Dado que a chamada ao modelo retorna <respostas> em sequência (simulado em teste unitário)",
            "Quando o Merchant Agent processa um pedido",
            "Então o resultado é <resultado>",
            "E o número de chamadas ao modelo é <chamadas>"], "CA4 / CA5 / RN04",
         [("respostas", "resultado", "chamadas"), ("503, 200", "resposta normal", "2"),
          ("503, 503, 200", "resposta normal", "3"), ("503, 503, 503", "erro legível", "3"), ("400", "erro legível", "1")]),
    ],
    lacunas=[],
    premissas=["Os nomes exatos das mensagens de log serão definidos na implementação; os cenários verificam o conteúdo, não o texto literal."])

B4 = BASE.format(v="v4")
BDD["F-V4.2.1"] = dict(
    feature="Credentials Provider Agent lista as formas de pagamento da conta de demonstração",
    contexto=["Dado que o Space da v4 está em \"Running\"",
              "E a conta de demonstração de account_manager.py está carregada"],
    cenarios=[
        ("CT01", "positivo", "Lista de formas de pagamento da demo", [
            "Quando o Shopping Agent v1 pede as formas de pagamento da conta de demonstração",
            'Então a lista contém "American Express ending in 4444"'], "CA1"),
        ("CT02", "negativo", "Credentials Provider fora do ar", [
            "Dado que o processo do Credentials Provider Agent está parado",
            "Quando o usuário chega à etapa de forma de pagamento no ADK Web",
            "Então a conversa informa que não foi possível obter as formas de pagamento"], "CA2"),
        ("CT03", "seguranca", "Credentials Provider não é acessível de fora", [
            f"Quando é feito GET {B4}/a2a/credentials_provider/.well-known/agent-card.json",
            "Então a resposta é HTTP 404"], "RN01 (F-V4.2)"),
        ("CT04", "positivo", "Estado mantido após restart", [
            "Dado que uma forma de pagamento foi usada em uma compra da v4",
            "Quando o Space da v4 é reiniciado",
            "Então o log mostra restore com environment='v4'",
            "E a próxima compra usa a mesma conta de demonstração"], "Task: espelhamento no Supabase"),
    ],
    lacunas=[],
    premissas=["A conta de demonstração contém o cartão com alias \"American Express ending in 4444\" (account_manager.py). Os dados são fictícios do repositório e não devem ser trocados por dados reais."])

BDD["F-V4.3.1"] = dict(
    feature="Spike: publicação do ADK Web atrás do nginx",
    contexto=["Dado que a prova de conceito do spike está publicada no Space da v4"],
    cenarios=[
        ("CT01", "positivo", "ADK Web abre pelo Space", [
            f"Quando um visitante abre {B4}/dev-ui (ou o caminho definido no spike)",
            "Então a tela do ADK Web é exibida"], "CA2"),
        ("CT02", "positivo", "Decisão registrada", [
            "Quando o CLAUDE.md do branch homolog-v4 é revisado",
            "Então existe uma seção de decisão com pelo menos 2 alternativas, riscos e a alternativa escolhida"], "CA1 / RN01"),
    ],
    lacunas=["Spike: os cenários verificam só a entrega da investigação. Os comportamentos definitivos estão em F-V4.3.2."],
    premissas=["O caminho /dev-ui é o padrão do ADK Web; o spike pode definir outro."])

BDD["F-V4.3.2"] = dict(
    feature="Compra assistida ponta a ponta pelo ADK Web",
    contexto=["Dado que o ADK Web da v4 está aberto com o agente shopping_agent selecionado",
              "E Merchant, Credentials Provider e Processor Agents estão em execução"],
    cenarios=[
        ("CT01", "positivo", "Compra assistida concluída", [
            'Dado que o usuário pediu "I want to buy a coffee maker" e escolheu uma das opções',
            'E escolheu a forma de pagamento "American Express ending in 4444" e assinou o Payment Mandate',
            'Quando informa o OTP "123"',
            "Então a conversa mostra a confirmação da compra com o recibo"], "CA1 / RN02"),
        ("CT02", "negativo", "OTP incorreto", [
            "Dado que o usuário chegou ao desafio OTP",
            'Quando informa o OTP "000"',
            "Então o pagamento não é concluído",
            "E a conversa informa que o OTP é inválido"], "CA2 / RN02"),
        ("CT03", "negativo", "Usuário recusa o carrinho", [
            "Dado que o Merchant apresentou as opções de compra",
            "Quando o usuário responde que não quer nenhuma delas",
            "Então nenhum Payment Mandate é criado em ap2_env_mandates com environment='v4'"], "CA3 / RN01"),
        ("CT04", "positivo", "Mandates da compra registrados", [
            "Dado que o CT01 foi concluído às <hora_do_teste>",
            "Quando é consultado ap2_env_mandates com environment='v4' e first_seen_at posterior a <hora_do_teste>",
            "Então existe o Payment Mandate da compra"], "CA4 / RN03"),
        ("CT05", "seguranca", "ADK Web lista só o Shopping Agent v1", [
            "Quando o visitante abre o seletor de agentes do ADK Web",
            'Então a lista contém apenas "shopping_agent"'], "RN01 (F-V4.3)"),
        ("CT06", "performance", "Consumo do Gemini em uma compra assistida", [
            "Dado que nenhum outro teste usa a GOOGLE_API_KEY no período",
            "Quando o CT01 é executado 1 vez",
            "Então o pico de RPM no AI Studio é menor que 15"], "Métrica do épico"),
        ("CT07", "negativo", "Erro 503 temporário no Shopping Agent v1", [
            "Dado que a primeira chamada do Shopping Agent v1 ao modelo retorna 503 (simulado em teste unitário)",
            'Quando o usuário envia "I want to buy a coffee maker"',
            "Então a conversa continua com as opções de compra após a nova tentativa"], "CA5"),
    ],
    lacunas=["O limite de requisições do ADK Web depende da decisão do spike F-V4.3.1; o cenário será escrito depois dela."],
    premissas=['OTP de demonstração "123" conforme o README do cenário human-present.',
               "A conversa no ADK Web é em inglês até a tradução pt-BR alcançar o Shopping Agent v1."])

B5 = "https://ap2-homolog-v5-frontend.vercel.app"
BDD["F-V5.2.1"] = dict(
    feature="Spike: protocolo entre web client e Shopping Agent v1",
    contexto=["Dado que a prova de conceito está publicada na v5"],
    cenarios=[
        ("CT01", "positivo", "Contrato de artifacts documentado", [
            "Quando o CLAUDE.md do branch homolog-v5 é revisado",
            "Então há o contrato (tipos e campos) dos artifacts de cada etapa da jornada assistida"], "CA1 / RN01"),
        ("CT02", "positivo", "Primeiro artifact recebido pela tela", [
            f"Dado que {B5} está configurado para o Shopping Agent v1",
            "Quando o usuário envia a primeira mensagem na prova de conceito",
            "Então a tela recebe um artifact do tipo definido no contrato"], "CA2"),
    ],
    lacunas=["Spike: os comportamentos finais estão em F-V5.2.2 e F-V5.3.x."],
    premissas=[])

BDD["F-V5.2.2"] = dict(
    feature="Escolha entre jornada autônoma e assistida",
    contexto=[f"Dado que o usuário abre {B5}"],
    cenarios=[
        ("CT01", "positivo", "Tela inicial com as duas jornadas", [
            "Quando a página termina de carregar",
            'Então a tela mostra as opções "Compra autônoma" e "Compra assistida" com uma descrição curta de cada'], "CA1"),
        ("CT02", "positivo", "Jornada assistida usa o Shopping Agent v1", [
            'Dado que o usuário escolheu "Compra assistida"',
            'Quando envia a mensagem "I want to buy a coffee maker"',
            "Então a requisição A2A é enviada para a URL de VITE_ASSISTED_AGENT_URL"], "CA2 / RN02 (F-V5.2)"),
        ("CT03", "positivo", "Troca de jornada pede confirmação", [
            'Dado que o usuário está numa conversa da "Compra assistida"',
            'Quando escolhe "Compra autônoma"',
            "Então a tela pede confirmação para iniciar nova conversa"], "CA3 / RN02"),
        ("CT04", "positivo", "Troca confirmada inicia nova sessão", [
            "Dado que a tela pediu confirmação de troca de jornada",
            "Quando o usuário confirma",
            "Então a conversa anterior some da tela",
            "E a próxima mensagem é enviada com um sessionId diferente do anterior"], "CA3 / RN02"),
        ("CT05", "negativo", "Troca cancelada mantém a conversa", [
            "Dado que a tela pediu confirmação de troca de jornada",
            "Quando o usuário cancela",
            "Então a conversa atual continua exibida na mesma jornada"], "RN01"),
        ("CT06", "negativo", "Agente da jornada assistida fora do ar", [
            "Dado que o Shopping Agent v1 da v5 não responde",
            'Quando o usuário envia uma mensagem na "Compra assistida"',
            'Então a tela mostra uma mensagem iniciada por "Erro de conexão"',
            'E a opção "Compra autônoma" continua disponível'], "CA (F-V5.2)"),
        ("CT07", "regressao", "Compra autônoma no web client da v5", [
            'Dado que o usuário escolheu "Compra autônoma"',
            "Quando executa o roteiro de compra autônoma com price drop price=199 e stock=10",
            'Então a tela mostra "Compra concluída" com valor US$ 199,00'], "RN01 (F-V5.2)"),
    ],
    lacunas=[],
    premissas=['Os rótulos "Compra autônoma" e "Compra assistida" são sugestão; o texto final segue a tradução pt-BR.',
               'Textos da jornada autônoma conforme o PR #5 ("Compra concluída", "Erro de conexão"), validados no teste de aceitação de 27/09/2026.'])

BDD["F-V5.3.1"] = dict(
    feature="Seleção das opções de compra do Merchant",
    contexto=[f"Dado que o usuário está em {B5} na \"Compra assistida\""],
    cenarios=[
        ("CT01", "positivo", "Opções exibidas com os dados do Merchant", [
            'Quando o usuário envia "I want to buy a coffee maker" e o Merchant devolve 3 opções',
            "Então a tela mostra 3 cartões, cada um com nome, preço e comerciante"], "CA1 / RN01"),
        ("CT02", "positivo", "Escolha de uma opção avança o fluxo", [
            "Dado que a tela mostra as opções de compra",
            "Quando o usuário escolhe a primeira opção",
            "Então a escolha é enviada ao Shopping Agent v1",
            "E a etapa de forma de pagamento é exibida"], "CA2"),
        ("CT03", "borda", "Nenhuma opção retornada", [
            "Quando o Merchant devolve 0 opções",
            "Então a tela mostra mensagem de que não há opções",
            "E o usuário pode enviar um novo pedido"], "CA3"),
        ("CT04", "borda", "Apenas uma opção pode ser escolhida", [
            "Dado que o usuário escolheu a primeira opção",
            "Quando tenta escolher a segunda opção",
            "Então a seleção da segunda opção não é enviada ao agente"], "RN02"),
        ("CT05", "borda", "Formato de preço em dólar", [
            "Quando o Merchant devolve uma opção com preço <valor> USD",
            "Então a tela exibe <exibido>"], "RN03 (F-V5.3)",
         [("valor", "exibido"), ("450", "US$ 450,00"), ("1234.5", "US$ 1.234,50"), ("0.99", "US$ 0,99")]),
    ],
    lacunas=[],
    premissas=["O Merchant devolve 3 opções no CT01; o número real depende do catálogo gerado pelo sample."])

BDD["F-V5.3.2"] = dict(
    feature="Forma de pagamento e assinatura do Payment Mandate na Trusted Surface",
    contexto=[f"Dado que o usuário escolheu uma opção de compra de US$ 450,00 em {B5}"],
    cenarios=[
        ("CT01", "positivo", "Formas de pagamento da conta de demonstração", [
            "Quando a etapa de forma de pagamento é exibida",
            'Então a lista contém "American Express ending in 4444"'], "CA1"),
        ("CT02", "positivo", "Trusted Surface mostra os dados da compra", [
            'Dado que o usuário escolheu "American Express ending in 4444"',
            "Quando a Trusted Surface é exibida",
            "Então ela mostra o item, o valor US$ 450,00, o comerciante e a forma de pagamento"], "CA2 / RN01"),
        ("CT03", "negativo", "Recusa na Trusted Surface", [
            "Dado que a Trusted Surface está exibida",
            'Quando o usuário clica em "Recusar"',
            "Então a compra é encerrada",
            "E nenhum Payment Mandate aparece na aba Mandates"], "CA3 / RN02"),
        ("CT04", "positivo", "Assinatura gera o Payment Mandate", [
            "Dado que a Trusted Surface está exibida",
            'Quando o usuário clica em "Aprovar e assinar"',
            "Então o Payment Mandate aparece na aba Mandates"], "CA4"),
        ("CT05", "seguranca", "Valor assinado igual ao valor exibido", [
            "Dado que a Trusted Surface exibiu o valor US$ 450,00",
            'Quando o usuário clica em "Aprovar e assinar"',
            "Então o Payment Mandate decodificado na aba Mandates tem o valor 45000 centavos em USD"], "RN01"),
        ("CT06", "negativo", "Página recarregada antes da assinatura", [
            "Dado que a Trusted Surface está exibida",
            "Quando o usuário recarrega a página",
            "Então nenhum pagamento é iniciado"], "RN02"),
    ],
    lacunas=[],
    premissas=["O valor no Payment Mandate segue a convenção de centavos da v2 (amount_range em centavos); confirmar no contrato do spike F-V5.2.1."])

BDD["F-V5.3.3"] = dict(
    feature="Desafio OTP e recibo da compra assistida",
    contexto=[f"Dado que o usuário assinou o Payment Mandate de US$ 450,00 em {B5}",
              "E a tela mostra o desafio OTP"],
    cenarios=[
        ("CT01", "positivo", "OTP correto mostra o recibo", [
            'Quando o usuário informa "123" e confirma',
            "Então a tela mostra o recibo com número do pedido, valor US$ 450,00 e forma de pagamento"], "CA1"),
        ("CT02", "negativo", "OTP errado permite nova tentativa", [
            'Quando o usuário informa "000" e confirma',
            "Então a tela mostra erro de OTP inválido",
            "E o campo de OTP continua disponível"], "CA2"),
        ("CT03", "borda", "Campo OTP aceita só dígitos", [
            "Quando o usuário digita <entrada> no campo OTP",
            "Então o botão de confirmar fica <estado>"], "RN01",
         [("entrada", "estado"), ('"123"', "habilitado"), ('"12a"', "desabilitado"), ('"" (vazio)', "desabilitado")]),
        ("CT04", "negativo", "Três OTPs errados encerram a compra", [
            'Dado que o usuário informou "000" duas vezes',
            'Quando informa "000" pela terceira vez',
            "Então a compra é encerrada",
            "E nenhum recibo é exibido"], "CA3 / RN02 (proposta)"),
    ],
    lacunas=["CT04 depende da confirmação da RN02 (limite de 3 tentativas), que é proposta e não vem do repositório. Está marcado com @pendente-confirmacao."],
    premissas=['OTP de demonstração "123".'])

B6 = BASE.format(v="v6")
BDD["F-V6.2.1"] = dict(
    feature="Binários Go no container com seleção de backend",
    contexto=["Dado que o Dockerfile da v6 tem o estágio de build Go"],
    cenarios=[
        ("CT01", "positivo", "Build do Space com os binários Go", [
            "Quando o build do Space da v6 termina",
            'Então o estado do Space é "Running"',
            "E os binários Go estão presentes na imagem final"], "CA1 / RN01"),
        ("CT02", "positivo", "Seleção do backend por variável", [
            "Dado que AP2_BACKEND_LANG é <valor>",
            "Quando o Space inicia",
            "Então o log mostra os agentes de 8001–8003 iniciados em <linguagem>"], "CA2 / CA3 / RN01 (F-V6.2)",
         [("valor", "linguagem"), ("python", "Python"), ("go", "Go"), ("(ausente)", "Python")]),
        ("CT03", "negativo", "Valor inválido volta para Python com aviso", [
            'Dado que AP2_BACKEND_LANG é "rust"',
            "Quando o Space inicia",
            "Então o log mostra aviso de valor inválido",
            "E os agentes de 8001–8003 são iniciados em Python"], "CA3"),
    ],
    lacunas=[], premissas=["O aviso de valor inválido é texto livre no log; o cenário verifica a existência do aviso."])

BDD["F-V6.2.2"] = dict(
    feature="Compra assistida com backend Go",
    contexto=["Dado que o Space da v6 está com AP2_BACKEND_LANG=go",
              "E o usuário está na \"Compra assistida\" do web client apontado para a v6"],
    cenarios=[
        ("CT01", "positivo", "Compra concluída com backend Go", [
            'Dado que o usuário escolheu uma opção e "American Express ending in 4444" e assinou o Payment Mandate',
            'Quando informa o OTP "123"',
            "Então a tela mostra o recibo da compra"], "CA1"),
        ("CT02", "positivo", "Mandates registrados na v6", [
            "Dado que o CT01 foi concluído às <hora_do_teste>",
            "Quando é consultado ap2_env_mandates com environment='v6' e first_seen_at posterior a <hora_do_teste>",
            "Então existe o Payment Mandate da compra"], "CA2"),
        ("CT03", "negativo", "OTP errado com backend Go", [
            'Quando o usuário informa o OTP "000"',
            "Então o pagamento não é concluído"], "RN01 (mesmo roteiro da v4/v5)"),
    ],
    lacunas=["Se os agentes Go gravarem estado fora de TEMP_DB_DIR, o CT02 precisa de ajuste (premissa do épico)."],
    premissas=["Os agentes Go usam a mesma conta de demonstração e o mesmo OTP 123 dos agentes Python; confirmar no código Go."])

BDD["F-V6.3.1"] = dict(
    feature="App Android usando o backend público sem chave no APK",
    contexto=["Dado que o APK de homologação da v6 está instalado em um aparelho físico com internet"],
    cenarios=[
        ("CT01", "positivo", "App conecta ao Space por HTTPS", [
            'Quando o usuário envia "I want to buy a coffee maker" no app',
            f"Então as requisições ao Merchant vão para {B6} por HTTPS",
            "E o app mostra as opções de compra"], "CA1 / RN01"),
        ("CT02", "seguranca", "APK sem chave do Gemini", [
            "Dado o arquivo APK publicado",
            'Quando o APK é descompactado e é feita a busca pelo padrão de chave do Google ("AIza")',
            "Então nenhuma ocorrência é encontrada"], "CA2 / RN01 (F-V6.3)"),
        ("CT03", "negativo", "Backend fora do ar", [
            "Dado que o Space da v6 está parado",
            "Quando o usuário envia uma mensagem no app",
            "Então o app mostra erro de conexão"], "CA3"),
        ("CT04", "seguranca", "Conexão sem HTTPS é recusada", [
            f'Dado que a URL do Merchant no build é "http://ds-fabiopinheiro-ap2-homolog-v6.hf.space/a2a/merchant_agent"',
            "Quando o usuário envia uma mensagem no app",
            "Então o app não envia a requisição e mostra erro de configuração"], "RN02 (F-V6.3)"),
        ("CT05", "seguranca", "Limite de requisições no proxy do Gemini", [
            "Dado que o proxy do Gemini tem limite de <limite> requisições por minuto por visitante",
            "Quando o mesmo aparelho envia <limite>+1 requisições em 1 minuto",
            "Então a última resposta é HTTP 429"], "RN02"),
    ],
    lacunas=["O limite do proxy do Gemini (CT05) não está definido; <limite> precisa ser decidido antes do teste."],
    premissas=['O prefixo "AIza" é o formato atual das chaves de API do Google; ajustar a busca se o formato mudar.'])

BDD["F-V6.3.2"] = dict(
    feature="APK de homologação publicado no GitHub Releases",
    contexto=["Dado que o workflow de build do APK existe no branch homolog-v6"],
    cenarios=[
        ("CT01", "positivo", "Tag gera o APK na release", [
            "Quando a tag v6.0.1 é enviada ao repositório",
            'Então a release "v6.0.1" contém um arquivo APK com "6.0.1" no nome'], "CA1 / RN01"),
        ("CT02", "negativo", "Push sem tag não publica release", [
            "Quando um commit é enviado ao branch homolog-v6 sem tag",
            "Então nenhuma release nova é criada"], "RN01"),
        ("CT03", "positivo", "Instalação em aparelho físico", [
            "Dado um aparelho Android 8.0 ou superior (minSdk 26) com instalação de fontes externas permitida",
            "Quando o APK da release é instalado",
            "Então o app abre na tela inicial"], "CA2"),
        ("CT04", "positivo", "Compra com Digital Payment Credential", [
            "Dado um aparelho físico compatível com Credential Manager e DPC",
            "Quando o usuário conclui uma compra no app e autoriza com a credencial digital",
            "Então o app mostra a confirmação da compra"], "CA3"),
    ],
    lacunas=["Os requisitos de aparelho para DPC não estão documentados no repositório; o CT04 depende de um aparelho validado previamente."],
    premissas=["minSdk 26 lido de android/shopping_assistant/app/build.gradle.kts."])
