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
