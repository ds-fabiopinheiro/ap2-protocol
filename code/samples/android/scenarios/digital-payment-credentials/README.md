# Sample AP2: autorização do usuário com Digital Payment Credentials

Este sample mostra a autenticação do usuário em uma compra usando digital
payment credentials (DPC, credenciais digitais de pagamento).

## Cenário

Este repositório mostra um assistente de compras conversacional para Android.
Ele cobre a experiência completa do usuário, da busca de produtos em linguagem
natural (com Gemini) ao pagamento seguro com Digital Payment Credentials (DPC).
Toda a comunicação com o backend usa o protocolo A2A.

## Atores principais

Este sample é composto por:

*   **Shopping Agent:** um app Android que trata os pedidos de compra do usuário.
*   **Merchant Agent:** um agente que atende as consultas de produtos do shopping
    agent e verifica a assinatura da DPC. Roda localmente na porta `8001`.
*   **Credentials Provider Agent:** um agente que extrai a chave pública do
    Agent Provider do certificado da DPC e assina / fornece credenciais de
    pagamento. Roda localmente na porta `8002` (iniciado automaticamente pelo
    `run.sh`).

## Principais recursos

*   Compra com uma **Digital Payment Credential (DPC):** fluxo de pagamento
    moderno e seguro que usa o Android Credential Manager e permite assinar a
    intenção do usuário exibida em uma trusted surface.

## Como executar o exemplo

### Configuração

1.  **Instale o Android Studio.**

    Baixe o Android Studio no
    [site oficial](https://developer.android.com/studio) e instale-o.
    Isso instala o Android SDK, o JDK e as demais ferramentas necessárias
    para compilar e executar o app Android.

2.  **Obtenha uma chave de API do Google no
    [Google AI Studio](https://aistudio.google.com/apikey)** e exporte-a
    como variável de ambiente (necessária para os servidores do merchant /
    credentials provider):

    ```sh
    export GOOGLE_API_KEY=your_key
    ```

3.  **Crie o `local.properties` do app Android.**

    Este arquivo está no gitignore porque contém caminhos específicos da
    máquina e sua chave de API. Crie-o com sua chave e o caminho do Android
    SDK — o caminho do SDK aparece no Android Studio em `Settings > Languages &
    Frameworks > Android SDK`:

    ```sh
    cat > code/samples/android/shopping_assistant/local.properties <<EOF
    GEMINI_API_KEY=your_key
    sdk.dir=/absolute/path/to/Android/sdk
    EOF
    ```

4.  **Defina `JAVA_HOME`.**

    O JDK vem com o Android Studio, mas `JAVA_HOME` não é definido por
    padrão. O caminho aparece no Android Studio em `Settings >
    Build, Execution, Deployment > Build Tools > Gradle`:

    ```sh
    export JAVA_HOME=</absolute/path/to/jdk>
    ```

5.  **Gere o Gradle wrapper.**

    O Gradle wrapper (`gradlew`, `gradlew.bat`, `gradle/wrapper/*`) está no
    gitignore, então um clone novo não o inclui. Gere-o uma vez de uma
    destas formas:

    *   Abra `code/samples/android/shopping_assistant/` no Android Studio
        e aguarde a sincronização — o Android Studio gera o wrapper
        automaticamente, **ou**
    *   Execute a tarefa `wrapper` com um Gradle instalado no sistema:

        ```sh
        cd code/samples/android/shopping_assistant
        gradle wrapper
        cd -
        ```

6.  **Confirme que o ambiente atende aos
    [pré-requisitos do sample em Python](../../../python).**

7.  **Ative a Enhanced Payment Confirmation UI.**

    Para usar o fluxo de pagamento mais moderno e seguro, é preciso ativar
    uma feature flag obrigatória:

    **Inscreva-se no
    [Google Play Services Beta Program](https://developers.google.com/android/guides/beta-program):**
    confirme que a Conta Google do dispositivo de teste está inscrita.

8.  **Instale o app de carteira digital (sideload).**

    Esta demo exige um app de carteira digital separado ('CM Wallet'),
    instalado no mesmo dispositivo, que guarda as Digital Payment Credentials.

    1.  Baixe o
        [APK mais recente do CM Wallet](https://github.com/digitalcredentialsdev/CMWallet/actions?query=branch%3Amain).

    1.  Instale o APK e inicie o app:

        ```sh
        adb install app-debug.apk
        adb shell am start -n "com.credman.cmwallet/.MainActivity"
        ```

### Execução

Há um script que compila, instala e abre o app Android e inicia os
servidores locais do merchant e do credentials provider. Execute-o a partir
da raiz do repositório:

```sh
./code/samples/android/scenarios/digital-payment-credentials/run.sh
```

## Como usar o app

1.  Confirme que o servidor local do Merchant Agent está em execução:

    ```
    curl http://localhost:8001/a2a/merchant_agent/.well-known/agent-card.json
    ```

2.  Abra o app Shopping Assistant no dispositivo.

3.  Na tela de configurações do app, informe a URL do servidor local do
    merchant. A URL padrão é `http://10.0.2.2:8001`.

4.  Clique no botão **Connect**. O app busca o A2A Agent Card no servidor e
    inicia a sessão de chat.

5.  Agora você pode conversar com o assistente de compras. Por exemplo,
    diga: "I'm looking for a new car."
