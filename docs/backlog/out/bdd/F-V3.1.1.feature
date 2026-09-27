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
