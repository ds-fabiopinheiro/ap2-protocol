# Backlog das evoluções v3–v6 do ambiente de homologação do AP2

Repositório: `ds-fabiopinheiro/ap2-protocol` · Levantamento: 26/09/2026 · Status: **preview, nada foi criado no GitHub**.

Este pacote contém quatro épicos, um por versão. Cada versão tem um branch próprio (`homolog-v3` … `homolog-v6`), criado a partir da versão anterior. Com isso cada versão acumula as anteriores, e as anteriores continuam publicadas para comparação.

> **Nomes de versão.** "Shopping Agent v1" e "Shopping Agent v2" são nomes dos agentes no repositório do Google. As versões v3–v6 deste backlog são versões do **ambiente de homologação**. A versão atual publicada (`homolog-deploy`) é tratada como **v2**.

## 1. Linha de versões

| Versão | Branch | Criado a partir de | Space (backend) | Frontend (Vercel) | O que passa a existir |
|---|---|---|---|---|---|
| v2 (atual) | `homolog-deploy` | `main` | `ap2-homolog-backend` | `ap2-homolog-frontend` | Shopping Agent v2, jornada autônoma (human-not-present) |
| v3 | `homolog-v3` | `homolog-deploy` | `ap2-homolog-v3` | — (sem mudança de tela) | Merchant Agent e Merchant Payment Processor Agent via A2A; modelo configurável nos agentes A2A |
| v4 | `homolog-v4` | `homolog-v3` | `ap2-homolog-v4` | — (usa ADK Web) | Shopping Agent v1 e Credentials Provider Agent; compra assistida pelo ADK Web |
| v5 | `homolog-v5` | `homolog-v4` | `ap2-homolog-v5` | `ap2-homolog-v5-frontend` | Jornada assistida (human-present) no web client React, ao lado da autônoma |
| v6 | `homolog-v6` | `homolog-v5` | `ap2-homolog-v6` | usa o da v5 | Agentes em Go como backend alternativo; APK Android de homologação |

Ordem pedida pelo usuário para os épicos: Shopping Agent v1, Merchant Agent, Go e Android, jornada assistida. A ordem acima foi ajustada por dependência técnica: o Shopping Agent v1 chama o Merchant Agent (`remote_agents.py`), e a jornada assistida no web client precisa do Shopping Agent v1 publicado. É uma sugestão; a priorização é decisão do time.

## 2. Estratégia de branches

```mermaid
gitGraph
  commit id: "main (Google)"
  branch homolog-deploy
  commit id: "v2 publicada"
  branch homolog-v3
  commit id: "EP-V3"
  commit id: "tag v3.0.0"
  branch homolog-v4
  commit id: "EP-V4"
  commit id: "tag v4.0.0"
  branch homolog-v5
  commit id: "EP-V5"
  commit id: "tag v5.0.0"
  branch homolog-v6
  commit id: "EP-V6"
  commit id: "tag v6.0.0"
```

Regras:

1. **Criação.** Cada `homolog-vN` nasce do último commit de `homolog-v(N-1)` (a v3 nasce de `homolog-deploy`). A versão anterior não recebe código da nova.
2. **Tasks.** Cada task é feita em `task/vN-<nº da issue>-<resumo>` e entra por PR em `homolog-vN`. O PR cita a issue (`Closes #nº`).
3. **Fechamento.** A versão fecha com a tag `vN.0.0` no último commit do branch. Correções depois disso usam `vN.0.1`, `vN.0.2`...
4. **Correções nas anteriores.** Se uma correção valer para versões anteriores, ela é feita na mais antiga afetada e levada adiante por PR (`homolog-v3` → `homolog-v4` → …).
5. **Atualizações do Google.** Ficam num branch separado, como o usuário definiu. A incorporação em uma versão é uma task própria da versão.
6. **`main`.** Não é alterado.

## 3. Ambiente de cada versão

| Recurso | Como fica por versão | Motivo |
|---|---|---|
| HF Space | Um Space por versão (`ap2-homolog-vN`), com o mesmo Dockerfile e `AP2_REF=homolog-vN` | A versão anterior continua acessível; o Dockerfile já aceita `AP2_REF` |
| Rebuild | `hf-space-rebuild.yml` mapeia branch → Space | Hoje o workflow só conhece `homolog-deploy` |
| Vercel | Um projeto por versão com mudança de tela (v5) | URLs de preview exigem login na proteção padrão; um projeto por versão mantém a URL pública |
| Supabase | Mesmo projeto `ap2-homolog-db`; tabelas `ap2_env_*` com coluna `environment` e variável `AP2_ENV` | Evita que dois Spaces sobrescrevam o mesmo `ap2_state_files`; não cria custo de branching do Supabase |
| Migrations | Entram também em `homolog-deploy` por PR separado | A integração do Supabase só aplica migrations desse branch |
| Chave do Gemini | Mesma `GOOGLE_API_KEY` em todos os Spaces | A cota do plano gratuito (15 RPM, 500 RPD) é compartilhada entre as versões |

## 4. Organização no GitHub

| Elemento | Uso |
|---|---|
| Labels de tipo | `tipo:épico`, `tipo:feature`, `tipo:pbi`, `tipo:task` |
| Labels de área (tasks) | `área:back`, `área:front`, `área:infra`, `área:qa`, `área:docs`, `área:mobile`, `área:segurança` |
| Labels de versão | `versão:v3` … `versão:v6` |
| Milestones | Um por versão (ex.: "v3 — Merchant Agent (homolog-v3)") |
| Hierarquia | Sub-issues do GitHub: Épico → Feature → PBI → Task |
| Corpo da issue | Seções padronizadas (Campos, Descrição, Regras, Fora de escopo, Critérios de aceite, Definição de pronto) |
| GitHub Projects (opcional) | Campos Status, Estimativa e Iteração preenchidos no Project; o script não preenche esses campos |

Os tipos de issue nativos do GitHub (Epic, Feature, Task) só existem em organizações. Como o repositório é de conta pessoal, o tipo fica em label.

## 5. Números

| Versão | Features | PBIs | Tasks | Story points | Horas |
|---|---|---|---|---|---|
| v3 | 3 | 5 | 20 | 26 | 70 |
| v4 | 3 | 4 | 15 | 19 | 47 |
| v5 | 3 | 6 | 22 | 29 | 79 |
| v6 | 3 | 5 | 18 | 28 | 64 |
| **Total** | **12** | **20** | **75** | **102** | **260** |

Total de issues: 111.

Estimativas em story points (PBI) e horas (task) são sugestões para o time validar.

## 6. Árvore

```
📊 EP-V3 · v3 · Merchant Agent e Merchant Payment Processor Agent publicados via A2A  (branch homolog-v3)
├── 🎯 F-V3.1 · Ambiente e branch da v3
│   └── 📋 F-V3.1.1 · Ambiente de homologação v3 publicado a partir do branch homolog-v3 · 8 pts
│       ├── ✅ [Infra] Criar o branch homolog-v3 a partir de homolog-deploy · 1 h
│       ├── ✅ [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v3 (Docker, CPU Basic, Protected) · 3 h
│       ├── ✅ [Back] Isolar o estado de cada versão no Supabase (AP2_ENV) · 8 h
│       ├── ✅ [Infra] Aplicar a migration de isolamento no projeto ap2-homolog-db · 2 h
│       ├── ✅ [Infra] Incluir o mapeamento homolog-v3 → ds-fabiopinheiro/ap2-homolog-v3 no workflow de rebuild · 3 h
│       ├── ✅ [QA] Verificar que as versões anteriores continuam funcionando após a criação da v3 · 3 h
│       └── ✅ [Docs] Registrar a v3 no CLAUDE.md e no deploy/README.md · 2 h
├── 🎯 F-V3.2 · Merchant Agent publicado como serviço A2A
│   ├── 📋 F-V3.2.1 · Merchant Agent acessível por A2A com agent card público · 5 pts
│   │   ├── ✅ [Back] Iniciar o Merchant Agent no start.sh da v3 · 3 h
│   │   ├── ✅ [Back] Reescrever a URL do agent card do Merchant Agent · 2 h
│   │   ├── ✅ [Infra] Adicionar a rota /a2a/merchant_agent no nginx com limite de requisições · 3 h
│   │   └── ✅ [QA] Testar agent card, limite e reinício do Merchant Agent · 3 h
│   └── 📋 F-V3.2.2 · Busca de produto no Merchant Agent com resposta assinada · 5 pts
│       ├── ✅ [QA] Escrever script de teste A2A para o Merchant Agent · 8 h
│       ├── ✅ [Back] Levar o watch.log dos agentes para LOGS_DIR · 2 h
│       ├── ✅ [Back] Registrar no Supabase os mandates emitidos pelo Merchant Agent · 5 h
│       └── ✅ [QA] Executar o teste 3 vezes e medir o consumo do Gemini · 2 h
└── 🎯 F-V3.3 · Merchant Payment Processor Agent e modelo configurável nos agentes A2A
    ├── 📋 F-V3.3.1 · Merchant Payment Processor Agent em execução interna com desafio OTP · 3 pts
    │   ├── ✅ [Back] Iniciar o Processor Agent no start.sh da v3 · 2 h
    │   └── ✅ [QA] Verificar isolamento e reinício do Processor Agent · 2 h
    └── 📋 F-V3.3.2 · Modelo dos agentes A2A definido por AGENT_MODEL · 5 pts
        ├── ✅ [Back] Ler AGENT_MODEL em function_call_resolver.py e base_server_executor.py · 8 h
        ├── ✅ [Back] Aplicar a regra de nova tentativa em erro 503 nos agentes A2A · 5 h
        └── ✅ [QA] Testar a troca de modelo e a nova tentativa nos agentes A2A · 3 h
📊 EP-V4 · v4 · Shopping Agent v1 e Credentials Provider Agent com jornada assistida no ADK Web  (branch homolog-v4)
├── 🎯 F-V4.1 · Ambiente e branch da v4
│   └── 📋 F-V4.1.1 · Ambiente de homologação v4 publicado a partir do branch homolog-v4 · 5 pts
│       ├── ✅ [Infra] Criar o branch homolog-v4 a partir de homolog-v3 · 1 h
│       ├── ✅ [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v4 (Docker, CPU Basic, Protected) · 3 h
│       ├── ✅ [Infra] Incluir o mapeamento homolog-v4 → ds-fabiopinheiro/ap2-homolog-v4 no workflow de rebuild · 3 h
│       ├── ✅ [QA] Verificar que as versões anteriores continuam funcionando após a criação da v4 · 3 h
│       └── ✅ [Docs] Registrar a v4 no CLAUDE.md e no deploy/README.md · 2 h
├── 🎯 F-V4.2 · Credentials Provider Agent publicado internamente
│   └── 📋 F-V4.2.1 · Credentials Provider Agent lista as formas de pagamento da conta de demonstração · 3 pts
│       ├── ✅ [Back] Iniciar o Credentials Provider Agent no start.sh da v4 · 2 h
│       ├── ✅ [Back] Incluir os arquivos do Credentials Provider no espelhamento do Supabase · 3 h
│       └── ✅ [QA] Testar a listagem e a falha do Credentials Provider · 2 h
└── 🎯 F-V4.3 · Compra assistida com o Shopping Agent v1 no ADK Web
    ├── 📋 F-V4.3.1 · Spike: forma de publicar o ADK Web atrás do nginx · 3 pts
    │   ├── ✅ [Back] Testar ADK Web em subcaminho e em diretório de agentes dedicado · 5 h
    │   └── ✅ [Docs] Registrar a decisão sobre o ADK Web · 2 h
    └── 📋 F-V4.3.2 · Compra assistida ponta a ponta pelo ADK Web · 8 pts
        ├── ✅ [Back] Iniciar o ADK Web restrito ao Shopping Agent v1 · 5 h
        ├── ✅ [Infra] Rota e limite de requisições do ADK Web no nginx · 3 h
        ├── ✅ [Back] Persistir os mandates da jornada assistida no Supabase · 5 h
        ├── ✅ [Back] Alinhar o RetryingLlmAgent do Shopping Agent v1 à regra de retry da v2 · 3 h
        └── ✅ [QA] Executar os cenários de compra assistida · 5 h
📊 EP-V5 · v5 · Jornada assistida (human-present) no web client React  (branch homolog-v5)
├── 🎯 F-V5.1 · Ambiente e branch da v5
│   └── 📋 F-V5.1.1 · Ambiente de homologação v5 publicado a partir do branch homolog-v5 · 5 pts
│       ├── ✅ [Infra] Criar o branch homolog-v5 a partir de homolog-v4 · 1 h
│       ├── ✅ [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v5 (Docker, CPU Basic, Protected) · 3 h
│       ├── ✅ [Infra] Criar o projeto Vercel ap2-homolog-v5-frontend · 3 h
│       ├── ✅ [Infra] Incluir o mapeamento homolog-v5 → ds-fabiopinheiro/ap2-homolog-v5 no workflow de rebuild · 3 h
│       ├── ✅ [QA] Verificar que as versões anteriores continuam funcionando após a criação da v5 · 3 h
│       └── ✅ [Docs] Registrar a v5 no CLAUDE.md e no deploy/README.md · 2 h
├── 🎯 F-V5.2 · Integração do web client com o Shopping Agent v1
│   ├── 📋 F-V5.2.1 · Spike: protocolo entre web client e Shopping Agent v1 · 3 pts
│   │   ├── ✅ [Back] Avaliar expor o Shopping Agent v1 por A2A com run_server próprio · 5 h
│   │   ├── ✅ [Front] Avaliar o reaproveitamento de a2aClient.ts para o v1 · 3 h
│   │   └── ✅ [Docs] Registrar o contrato de artifacts da jornada assistida · 2 h
│   └── 📋 F-V5.2.2 · Escolha entre jornada autônoma e assistida na tela inicial · 3 pts
│       ├── ✅ [Front] Criar seletor de jornada e roteamento de agente · 5 h
│       ├── ✅ [Infra] Cadastrar VITE_ASSISTED_AGENT_URL no projeto Vercel da v5 · 1 h
│       └── ✅ [QA] Testar troca de jornada e regressão da autônoma · 3 h
└── 🎯 F-V5.3 · Telas da jornada assistida no web client
    ├── 📋 F-V5.3.1 · Seleção das opções de compra do Merchant · 5 pts
    │   ├── ✅ [Front] Criar o cartão de opções de compra · 5 h
    │   ├── ✅ [Back] Emitir o artifact de opções no Shopping Agent v1 · 5 h
    │   └── ✅ [QA] Testar seleção e lista vazia · 3 h
    ├── 📋 F-V5.3.2 · Escolha da forma de pagamento e assinatura do Payment Mandate na Trusted Surface · 8 pts
    │   ├── ✅ [Front] Criar o cartão de formas de pagamento · 5 h
    │   ├── ✅ [Front] Adaptar a Trusted Surface para o Payment Mandate da jornada assistida · 8 h
    │   ├── ✅ [Back] Emitir os artifacts de formas de pagamento e de pedido de assinatura · 5 h
    │   └── ✅ [QA] Testar assinatura e recusa · 3 h
    └── 📋 F-V5.3.3 · Desafio OTP e recibo da compra assistida · 5 pts
        ├── ✅ [Front] Criar o cartão de OTP e reaproveitar o ReceiptCard · 5 h
        ├── ✅ [Back] Aplicar o limite de tentativas de OTP (se RN02 for confirmada) · 3 h
        └── ✅ [QA] Testar OTP correto, errado e limite · 3 h
📊 EP-V6 · v6 · Agentes em Go e app Android de demonstração  (branch homolog-v6)
├── 🎯 F-V6.1 · Ambiente e branch da v6
│   └── 📋 F-V6.1.1 · Ambiente de homologação v6 publicado a partir do branch homolog-v6 · 5 pts
│       ├── ✅ [Infra] Criar o branch homolog-v6 a partir de homolog-v5 · 1 h
│       ├── ✅ [Infra] Criar o Space ds-fabiopinheiro/ap2-homolog-v6 (Docker, CPU Basic, Protected) · 3 h
│       ├── ✅ [Infra] Incluir o mapeamento homolog-v6 → ds-fabiopinheiro/ap2-homolog-v6 no workflow de rebuild · 3 h
│       ├── ✅ [QA] Verificar que as versões anteriores continuam funcionando após a criação da v6 · 3 h
│       └── ✅ [Docs] Registrar a v6 no CLAUDE.md e no deploy/README.md · 2 h
├── 🎯 F-V6.2 · Agentes Go como backend alternativo do cenário assistido
│   ├── 📋 F-V6.2.1 · Binários Go no container com seleção de backend · 5 pts
│   │   ├── ✅ [Infra] Adicionar estágio de build Go ao Dockerfile · 5 h
│   │   ├── ✅ [Back] Selecionar Python ou Go no start.sh por AP2_BACKEND_LANG · 3 h
│   │   └── ✅ [QA] Testar os três valores de AP2_BACKEND_LANG · 2 h
│   └── 📋 F-V6.2.2 · Compra assistida com backend Go · 5 pts
│       ├── ✅ [QA] Executar o roteiro de compra assistida com backend Go · 5 h
│       └── ✅ [Docs] Registrar diferenças observadas entre Python e Go · 2 h
└── 🎯 F-V6.3 · App Android de homologação usando o backend público
    ├── 📋 F-V6.3.1 · App Android configurado para o backend público sem chave no APK · 8 pts
    │   ├── ✅ [Mobile] Parametrizar as URLs do backend no build do app · 5 h
    │   ├── ✅ [Back] Criar endpoint de proxy do Gemini para o app, com limite de requisições · 8 h
    │   ├── ✅ [Mobile] Trocar a chamada direta ao Gemini pelo proxy · 5 h
    │   ├── ✅ [Segurança] Verificar o APK contra segredos embutidos · 2 h
    │   └── ✅ [Infra] Expor as rotas do Merchant e do Credentials Provider do cenário Android no nginx · 3 h
    └── 📋 F-V6.3.2 · APK de homologação publicado no GitHub Releases · 5 pts
        ├── ✅ [Infra] Criar workflow de build do APK (Gradle) e publicação no Releases · 5 h
        ├── ✅ [QA] Testar instalação e compra com DPC em aparelho físico · 5 h
        └── ✅ [Docs] Escrever instruções de instalação do APK de homologação · 2 h
```

## 7. Ordem sugerida de execução

1. **EP-V3.** Cria o padrão de versões (branch, Space, isolamento no Supabase, rebuild por branch) usado por todas as outras. Publica o Merchant e o Processor, pré-requisitos do Shopping Agent v1.
2. **EP-V4.** O Shopping Agent v1 depende do Merchant (v3) e do Credentials Provider. O ADK Web permite validar a jornada assistida antes de investir em tela.
3. **EP-V5.** A tela React só vale a pena depois de a jornada funcionar no ADK Web. O spike F-V5.2.1 define o contrato de dados.
4. **EP-V6.** Go e Android dependem do cenário assistido estável. O APK exige resolver primeiro a chave do Gemini embutida.

## 8. Verificação da decomposição

- **Cobertura.** Os quatro pedidos do usuário estão cobertos: Merchant Agent (EP-V3), Shopping Agent v1 (EP-V4), jornada assistida (EP-V4 no ADK Web e EP-V5 no web client), Go e Android (EP-V6).
- **Feature com um único PBI.** As features de ambiente (F-V3.1 … F-V6.1) e a F-V4.2 têm um só PBI. Foram mantidas como feature para deixar o trabalho de ambiente visível em cada versão; podem ser rebaixadas a PBI do épico se o time preferir.
- **Spikes.** F-V4.3.1 e F-V5.2.1 são investigações com prova de conceito; os PBIs seguintes dependem da decisão deles.
- **Fatiamento.** A jornada assistida (F-V5.3) foi fatiada por passo do fluxo (opções → pagamento e assinatura → OTP e recibo); camadas técnicas ficam nas tasks.
- **Independência.** Os PBIs de uma mesma feature têm dependência declarada no campo "Depende de".

## 9. Premissas (precisam de confirmação)

- Os agentes do cenário human-present rodam no mesmo container sem conflito de portas (8001–8003 e 8080–8083).
- O plano gratuito do Hugging Face permite um Space CPU Basic por versão.
- O README do cenário human-present cita IntentMandate/CartMandate (vocabulário da v0.1 do AP2), mas o código atual usa `checkout_mandate`/`payment_mandate`. Os testes devem seguir o comportamento observado.
- Não verificado se os agentes em Go chamam o Gemini.
- O app Android lê `GEMINI_API_KEY` do `local.properties` e grava a chave no `BuildConfig`; as URLs são `http://localhost:8001/8002` fixas (`SettingsScreen.kt`, `ShoppingTools.kt`).
- O limite de 3 tentativas de OTP (F-V5.3.3, RN02) é proposta, não regra do repositório.
- Os agentes A2A do cenário human-present usam o modelo `gemini-3.1-flash-lite-preview` fixo em `common/function_call_resolver.py`.
- O Shopping Agent v1 e seus 3 sub-agentes usam `common/retrying_llm_agent.py` com `max_retries=5`: até 5 tentativas, repetindo o turno inteiro do agente em qualquer exceção, sem espera.

## 10. Pendências para sincronizar

- **Responsável, sprint/iteração e prioridade** de cada issue: não definidos.
- **Token `HF_TOKEN`** do GitHub: precisa de permissão de escrita em cada novo Space (ação do dono da conta).
- **Secrets de cada Space** (`GOOGLE_API_KEY`, `SUPABASE_SECRET_KEY`): cadastrados pelo dono da conta.
- **Faturamento Google** (caso OR_CCR_53, resposta prevista até 03/10/2026): define se a cota continua a do plano gratuito.
- **Tradução pt-BR** do web client: PR #5 aprovado no teste de aceitação da interface em 27/09/2026, com ajustes pedidos; PRs #6–#8 em andamento. Mesclar antes do EP-V5 para evitar conflito de textos.
- **Regra de nova tentativa do modelo** (503): definida no PR de backend que corrige os erros do teste de 27/09; a v3 (F-V3.3.2) e a v4 (F-V4.3.2) reutilizam essa regra.

## 11. Como criar as issues no GitHub

Pré-requisito: [GitHub CLI](https://cli.github.com/) instalada e autenticada (`gh auth login`) com permissão de escrita em issues.

```bash
cd docs/backlog    # no repositório (PR #9); no zip, a pasta é backlog/
python3 create_issues.py                  # simulação: lista o que seria criado
python3 create_issues.py --apply --only v3  # cria só o épico v3 e seus filhos
python3 create_issues.py --apply          # cria tudo
```

O script:

1. cria as labels e os milestones que faltam;
2. cria as issues na ordem pai → filho, com o corpo de `out/issues/*.md`;
3. vincula cada filho ao pai como sub-issue;
4. grava o mapa chave → número em `out/created.json` (arquivo local, ignorado pelo `.gitignore` da pasta).

Se for executado de novo, reaproveita issues com o mesmo título.

## 12. Cenários de teste (BDD)

Cada PBI tem um arquivo `.feature` em `out/bdd/` e a mesma seção "Cenários de teste (BDD)" no corpo da issue. Todos os critérios de aceite têm pelo menos um cenário (matriz em `out/bdd/README.md`). Os 20 arquivos foram validados com o parser Gherkin oficial (`gherkin-official`).

## 13. Arquivos

| Arquivo | Conteúdo |
|---|---|
| `README.md` | Este documento |
| `out/issues/NNN_<chave>.md` | Corpo de cada issue, com front matter (título, labels, milestone, pai) |
| `out/issues.json` | Índice das issues, usado pelo script |
| `out/table.md` | Tabela consolidada de todos os itens |
| `out/tree.txt` | Árvore da decomposição |
| `out/bdd/<PBI>.feature` | Cenários de teste em Gherkin pt-BR, um arquivo por PBI (101 cenários) |
| `out/bdd/README.md` | Preview dos testes: matriz de cobertura, lacunas e premissas por PBI |
| `data.py`, `bdd.py` | Fonte do backlog e dos cenários |
| `build_all.py` | Regera tudo (issues, cenários e este README) |
| `create_issues.py` | Criação no GitHub via `gh` |
