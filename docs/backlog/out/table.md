| # | Tipo | Chave | Título | Pai | Estimativa (sugestão) | Depende de |
|---|---|---|---|---|---|---|
| 1 | Épico | EP-V3 | v3 · Merchant Agent e Merchant Payment Processor Agent publicados via A2A | — | — | — |
| 2 | Feature | F-V3.1 | Ambiente e branch da v3 | EP-V3 | — | Secret HF_TOKEN com permissão no novo Space (ação do dono da conta)., Secrets do Space cadastrados pelo dono da conta. |
| 3 | PBI | F-V3.1.1 | Ambiente de homologação v3 publicado a partir do branch homolog-v3 | F-V3.1 | 8 pts | — |
| 4 | Task | F-V3.1.1.T1 | [Infra] Criar o branch homolog-v3 a partir de homolog-deploy | F-V3.1.1 | 1 h | — |
| 5 | Task | F-V3.1.1.T2 | [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v3 (Docker, CPU Basic, Protected) | F-V3.1.1 | 3 h | — |
| 6 | Task | F-V3.1.1.T3 | [Back] Isolar o estado de cada versão no Supabase (AP2_ENV) | F-V3.1.1 | 8 h | — |
| 7 | Task | F-V3.1.1.T4 | [Infra] Aplicar a migration de isolamento no projeto ap2-homolog-db | F-V3.1.1 | 2 h | — |
| 8 | Task | F-V3.1.1.T5 | [Infra] Incluir o mapeamento homolog-v3 → ds-fabiopinheiro/ap2-homolog-v3 no workflow de rebuild | F-V3.1.1 | 3 h | — |
| 9 | Task | F-V3.1.1.T6 | [QA] Verificar que as versões anteriores continuam funcionando após a criação da v3 | F-V3.1.1 | 3 h | — |
| 10 | Task | F-V3.1.1.T7 | [Docs] Registrar a v3 no CLAUDE.md e no deploy/README.md | F-V3.1.1 | 2 h | — |
| 11 | Feature | F-V3.2 | Merchant Agent publicado como serviço A2A | EP-V3 | — | F-V3.1 concluída. |
| 12 | PBI | F-V3.2.1 | Merchant Agent acessível por A2A com agent card público | F-V3.2 | 5 pts | F-V3.1.1 |
| 13 | Task | F-V3.2.1.T1 | [Back] Iniciar o Merchant Agent no start.sh da v3 | F-V3.2.1 | 3 h | — |
| 14 | Task | F-V3.2.1.T2 | [Back] Reescrever a URL do agent card do Merchant Agent | F-V3.2.1 | 2 h | — |
| 15 | Task | F-V3.2.1.T3 | [Infra] Adicionar a rota /a2a/merchant_agent no nginx com limite de requisições | F-V3.2.1 | 3 h | — |
| 16 | Task | F-V3.2.1.T4 | [QA] Testar agent card, limite e reinício do Merchant Agent | F-V3.2.1 | 3 h | — |
| 17 | PBI | F-V3.2.2 | Busca de produto no Merchant Agent com resposta assinada | F-V3.2 | 5 pts | F-V3.2.1 |
| 18 | Task | F-V3.2.2.T1 | [QA] Escrever script de teste A2A para o Merchant Agent | F-V3.2.2 | 8 h | — |
| 19 | Task | F-V3.2.2.T2 | [Back] Levar o watch.log dos agentes para LOGS_DIR | F-V3.2.2 | 2 h | — |
| 20 | Task | F-V3.2.2.T3 | [Back] Registrar no Supabase os mandates emitidos pelo Merchant Agent | F-V3.2.2 | 5 h | — |
| 21 | Task | F-V3.2.2.T4 | [QA] Executar o teste 3 vezes e medir o consumo do Gemini | F-V3.2.2 | 2 h | — |
| 22 | Feature | F-V3.3 | Merchant Payment Processor Agent e modelo configurável nos agentes A2A | EP-V3 | — | F-V3.1 concluída. |
| 23 | PBI | F-V3.3.1 | Merchant Payment Processor Agent em execução interna com desafio OTP | F-V3.3 | 3 pts | F-V3.1.1 |
| 24 | Task | F-V3.3.1.T1 | [Back] Iniciar o Processor Agent no start.sh da v3 | F-V3.3.1 | 2 h | — |
| 25 | Task | F-V3.3.1.T2 | [QA] Verificar isolamento e reinício do Processor Agent | F-V3.3.1 | 2 h | — |
| 26 | PBI | F-V3.3.2 | Modelo dos agentes A2A definido por AGENT_MODEL | F-V3.3 | 5 pts | F-V3.2.2 |
| 27 | Task | F-V3.3.2.T1 | [Back] Ler AGENT_MODEL em function_call_resolver.py e base_server_executor.py | F-V3.3.2 | 8 h | — |
| 28 | Task | F-V3.3.2.T2 | [Back] Aplicar a regra de nova tentativa em erro 503 nos agentes A2A | F-V3.3.2 | 5 h | — |
| 29 | Task | F-V3.3.2.T3 | [QA] Testar a troca de modelo e a nova tentativa nos agentes A2A | F-V3.3.2 | 3 h | — |
| 30 | Épico | EP-V4 | v4 · Shopping Agent v1 e Credentials Provider Agent com jornada assistida no ADK Web | — | — | EP-V3 |
| 31 | Feature | F-V4.1 | Ambiente e branch da v4 | EP-V4 | — | Secret HF_TOKEN com permissão no novo Space (ação do dono da conta)., Secrets do Space cadastrados pelo dono da conta. |
| 32 | PBI | F-V4.1.1 | Ambiente de homologação v4 publicado a partir do branch homolog-v4 | F-V4.1 | 5 pts | — |
| 33 | Task | F-V4.1.1.T1 | [Infra] Criar o branch homolog-v4 a partir de homolog-v3 | F-V4.1.1 | 1 h | — |
| 34 | Task | F-V4.1.1.T2 | [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v4 (Docker, CPU Basic, Protected) | F-V4.1.1 | 3 h | — |
| 35 | Task | F-V4.1.1.T3 | [Infra] Incluir o mapeamento homolog-v4 → ds-fabiopinheiro/ap2-homolog-v4 no workflow de rebuild | F-V4.1.1 | 3 h | — |
| 36 | Task | F-V4.1.1.T4 | [QA] Verificar que as versões anteriores continuam funcionando após a criação da v4 | F-V4.1.1 | 3 h | — |
| 37 | Task | F-V4.1.1.T5 | [Docs] Registrar a v4 no CLAUDE.md e no deploy/README.md | F-V4.1.1 | 2 h | — |
| 38 | Feature | F-V4.2 | Credentials Provider Agent publicado internamente | EP-V4 | — | F-V4.1 concluída. |
| 39 | PBI | F-V4.2.1 | Credentials Provider Agent lista as formas de pagamento da conta de demonstração | F-V4.2 | 3 pts | F-V4.1.1 |
| 40 | Task | F-V4.2.1.T1 | [Back] Iniciar o Credentials Provider Agent no start.sh da v4 | F-V4.2.1 | 2 h | — |
| 41 | Task | F-V4.2.1.T2 | [Back] Incluir os arquivos do Credentials Provider no espelhamento do Supabase | F-V4.2.1 | 3 h | — |
| 42 | Task | F-V4.2.1.T3 | [QA] Testar a listagem e a falha do Credentials Provider | F-V4.2.1 | 2 h | — |
| 43 | Feature | F-V4.3 | Compra assistida com o Shopping Agent v1 no ADK Web | EP-V4 | — | F-V4.2 concluída., Épico v3 concluído. |
| 44 | PBI | F-V4.3.1 | Spike: forma de publicar o ADK Web atrás do nginx | F-V4.3 | 3 pts | F-V4.1.1 |
| 45 | Task | F-V4.3.1.T1 | [Back] Testar ADK Web em subcaminho e em diretório de agentes dedicado | F-V4.3.1 | 5 h | — |
| 46 | Task | F-V4.3.1.T2 | [Docs] Registrar a decisão sobre o ADK Web | F-V4.3.1 | 2 h | — |
| 47 | PBI | F-V4.3.2 | Compra assistida ponta a ponta pelo ADK Web | F-V4.3 | 8 pts | F-V4.3.1, F-V4.2.1 |
| 48 | Task | F-V4.3.2.T1 | [Back] Iniciar o ADK Web restrito ao Shopping Agent v1 | F-V4.3.2 | 5 h | — |
| 49 | Task | F-V4.3.2.T2 | [Infra] Rota e limite de requisições do ADK Web no nginx | F-V4.3.2 | 3 h | — |
| 50 | Task | F-V4.3.2.T3 | [Back] Persistir os mandates da jornada assistida no Supabase | F-V4.3.2 | 5 h | — |
| 51 | Task | F-V4.3.2.T4 | [Back] Alinhar o RetryingLlmAgent do Shopping Agent v1 à regra de retry da v2 | F-V4.3.2 | 3 h | — |
| 52 | Task | F-V4.3.2.T5 | [QA] Executar os cenários de compra assistida | F-V4.3.2 | 5 h | — |
| 53 | Épico | EP-V5 | v5 · Jornada assistida (human-present) no web client React | — | — | EP-V4 |
| 54 | Feature | F-V5.1 | Ambiente e branch da v5 | EP-V5 | — | Secret HF_TOKEN com permissão no novo Space (ação do dono da conta)., Secrets do Space cadastrados pelo dono da conta. |
| 55 | PBI | F-V5.1.1 | Ambiente de homologação v5 publicado a partir do branch homolog-v5 | F-V5.1 | 5 pts | — |
| 56 | Task | F-V5.1.1.T1 | [Infra] Criar o branch homolog-v5 a partir de homolog-v4 | F-V5.1.1 | 1 h | — |
| 57 | Task | F-V5.1.1.T2 | [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v5 (Docker, CPU Basic, Protected) | F-V5.1.1 | 3 h | — |
| 58 | Task | F-V5.1.1.T3 | [Infra] Criar o projeto Vercel ap2-homolog-v5-frontend | F-V5.1.1 | 3 h | — |
| 59 | Task | F-V5.1.1.T4 | [Infra] Incluir o mapeamento homolog-v5 → ds-fabiopinheiro/ap2-homolog-v5 no workflow de rebuild | F-V5.1.1 | 3 h | — |
| 60 | Task | F-V5.1.1.T5 | [QA] Verificar que as versões anteriores continuam funcionando após a criação da v5 | F-V5.1.1 | 3 h | — |
| 61 | Task | F-V5.1.1.T6 | [Docs] Registrar a v5 no CLAUDE.md e no deploy/README.md | F-V5.1.1 | 2 h | — |
| 62 | Feature | F-V5.2 | Integração do web client com o Shopping Agent v1 | EP-V5 | — | F-V5.1 concluída. |
| 63 | PBI | F-V5.2.1 | Spike: protocolo entre web client e Shopping Agent v1 | F-V5.2 | 3 pts | F-V5.1.1 |
| 64 | Task | F-V5.2.1.T1 | [Back] Avaliar expor o Shopping Agent v1 por A2A com run_server próprio | F-V5.2.1 | 5 h | — |
| 65 | Task | F-V5.2.1.T2 | [Front] Avaliar o reaproveitamento de a2aClient.ts para o v1 | F-V5.2.1 | 3 h | — |
| 66 | Task | F-V5.2.1.T3 | [Docs] Registrar o contrato de artifacts da jornada assistida | F-V5.2.1 | 2 h | — |
| 67 | PBI | F-V5.2.2 | Escolha entre jornada autônoma e assistida na tela inicial | F-V5.2 | 3 pts | F-V5.2.1 |
| 68 | Task | F-V5.2.2.T1 | [Front] Criar seletor de jornada e roteamento de agente | F-V5.2.2 | 5 h | — |
| 69 | Task | F-V5.2.2.T2 | [Infra] Cadastrar VITE_ASSISTED_AGENT_URL no projeto Vercel da v5 | F-V5.2.2 | 1 h | — |
| 70 | Task | F-V5.2.2.T3 | [QA] Testar troca de jornada e regressão da autônoma | F-V5.2.2 | 3 h | — |
| 71 | Feature | F-V5.3 | Telas da jornada assistida no web client | EP-V5 | — | F-V5.2 concluída. |
| 72 | PBI | F-V5.3.1 | Seleção das opções de compra do Merchant | F-V5.3 | 5 pts | F-V5.2.2 |
| 73 | Task | F-V5.3.1.T1 | [Front] Criar o cartão de opções de compra | F-V5.3.1 | 5 h | — |
| 74 | Task | F-V5.3.1.T2 | [Back] Emitir o artifact de opções no Shopping Agent v1 | F-V5.3.1 | 5 h | — |
| 75 | Task | F-V5.3.1.T3 | [QA] Testar seleção e lista vazia | F-V5.3.1 | 3 h | — |
| 76 | PBI | F-V5.3.2 | Escolha da forma de pagamento e assinatura do Payment Mandate na Trusted Surface | F-V5.3 | 8 pts | F-V5.3.1 |
| 77 | Task | F-V5.3.2.T1 | [Front] Criar o cartão de formas de pagamento | F-V5.3.2 | 5 h | — |
| 78 | Task | F-V5.3.2.T2 | [Front] Adaptar a Trusted Surface para o Payment Mandate da jornada assistida | F-V5.3.2 | 8 h | — |
| 79 | Task | F-V5.3.2.T3 | [Back] Emitir os artifacts de formas de pagamento e de pedido de assinatura | F-V5.3.2 | 5 h | — |
| 80 | Task | F-V5.3.2.T4 | [QA] Testar assinatura e recusa | F-V5.3.2 | 3 h | — |
| 81 | PBI | F-V5.3.3 | Desafio OTP e recibo da compra assistida | F-V5.3 | 5 pts | F-V5.3.2 |
| 82 | Task | F-V5.3.3.T1 | [Front] Criar o cartão de OTP e reaproveitar o ReceiptCard | F-V5.3.3 | 5 h | — |
| 83 | Task | F-V5.3.3.T2 | [Back] Aplicar o limite de tentativas de OTP (se RN02 for confirmada) | F-V5.3.3 | 3 h | — |
| 84 | Task | F-V5.3.3.T3 | [QA] Testar OTP correto, errado e limite | F-V5.3.3 | 3 h | — |
| 85 | Épico | EP-V6 | v6 · Agentes em Go e app Android de demonstração | — | — | EP-V5 |
| 86 | Feature | F-V6.1 | Ambiente e branch da v6 | EP-V6 | — | Secret HF_TOKEN com permissão no novo Space (ação do dono da conta)., Secrets do Space cadastrados pelo dono da conta. |
| 87 | PBI | F-V6.1.1 | Ambiente de homologação v6 publicado a partir do branch homolog-v6 | F-V6.1 | 5 pts | — |
| 88 | Task | F-V6.1.1.T1 | [Infra] Criar o branch homolog-v6 a partir de homolog-v5 | F-V6.1.1 | 1 h | — |
| 89 | Task | F-V6.1.1.T2 | [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v6 (Docker, CPU Basic, Protected) | F-V6.1.1 | 3 h | — |
| 90 | Task | F-V6.1.1.T3 | [Infra] Incluir o mapeamento homolog-v6 → ds-fabiopinheiro/ap2-homolog-v6 no workflow de rebuild | F-V6.1.1 | 3 h | — |
| 91 | Task | F-V6.1.1.T4 | [QA] Verificar que as versões anteriores continuam funcionando após a criação da v6 | F-V6.1.1 | 3 h | — |
| 92 | Task | F-V6.1.1.T5 | [Docs] Registrar a v6 no CLAUDE.md e no deploy/README.md | F-V6.1.1 | 2 h | — |
| 93 | Feature | F-V6.2 | Agentes Go como backend alternativo do cenário assistido | EP-V6 | — | F-V6.1 concluída. |
| 94 | PBI | F-V6.2.1 | Binários Go no container com seleção de backend | F-V6.2 | 5 pts | F-V6.1.1 |
| 95 | Task | F-V6.2.1.T1 | [Infra] Adicionar estágio de build Go ao Dockerfile | F-V6.2.1 | 5 h | — |
| 96 | Task | F-V6.2.1.T2 | [Back] Selecionar Python ou Go no start.sh por AP2_BACKEND_LANG | F-V6.2.1 | 3 h | — |
| 97 | Task | F-V6.2.1.T3 | [QA] Testar os três valores de AP2_BACKEND_LANG | F-V6.2.1 | 2 h | — |
| 98 | PBI | F-V6.2.2 | Compra assistida com backend Go | F-V6.2 | 5 pts | F-V6.2.1 |
| 99 | Task | F-V6.2.2.T1 | [QA] Executar o roteiro de compra assistida com backend Go | F-V6.2.2 | 5 h | — |
| 100 | Task | F-V6.2.2.T2 | [Docs] Registrar diferenças observadas entre Python e Go | F-V6.2.2 | 2 h | — |
| 101 | Feature | F-V6.3 | App Android de homologação usando o backend público | EP-V6 | — | F-V6.1 concluída. |
| 102 | PBI | F-V6.3.1 | App Android configurado para o backend público sem chave no APK | F-V6.3 | 8 pts | F-V6.1.1 |
| 103 | Task | F-V6.3.1.T1 | [Mobile] Parametrizar as URLs do backend no build do app | F-V6.3.1 | 5 h | — |
| 104 | Task | F-V6.3.1.T2 | [Back] Criar endpoint de proxy do Gemini para o app, com limite de requisições | F-V6.3.1 | 8 h | — |
| 105 | Task | F-V6.3.1.T3 | [Mobile] Trocar a chamada direta ao Gemini pelo proxy | F-V6.3.1 | 5 h | — |
| 106 | Task | F-V6.3.1.T4 | [Segurança] Verificar o APK contra segredos embutidos | F-V6.3.1 | 2 h | — |
| 107 | Task | F-V6.3.1.T5 | [Infra] Expor as rotas do Merchant e do Credentials Provider do cenário Android no nginx | F-V6.3.1 | 3 h | — |
| 108 | PBI | F-V6.3.2 | APK de homologação publicado no GitHub Releases | F-V6.3 | 5 pts | F-V6.3.1 |
| 109 | Task | F-V6.3.2.T1 | [Infra] Criar workflow de build do APK (Gradle) e publicação no Releases | F-V6.3.2 | 5 h | — |
| 110 | Task | F-V6.3.2.T2 | [QA] Testar instalação e compra com DPC em aparelho físico | F-V6.3.2 | 5 h | — |
| 111 | Task | F-V6.3.2.T3 | [Docs] Escrever instruções de instalação do APK de homologação | F-V6.3.2 | 2 h | — |
