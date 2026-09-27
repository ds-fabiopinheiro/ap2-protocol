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
