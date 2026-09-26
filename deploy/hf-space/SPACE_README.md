---
title: AP2 Homolog Backend
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
short_description: Backend de homologação do Agent Payments Protocol (AP2)
---

# AP2 – backend de homologação

Backend do cenário `human-not-present / cards` do
[Agent Payments Protocol](https://github.com/ds-fabiopinheiro/ap2-protocol)
(branch `homolog-deploy`). O Dockerfile deste Space clona esse branch e executa
`deploy/hf-space/start.sh`.

| Rota pública | Serviço interno |
|---|---|
| `/a2a/shopping_agent` | Shopping Agent (ADK + A2A), porta 8080 |
| `/merchant/*` | Merchant trigger server (`/state`, `/trigger-price-drop`), porta 8081 |

Credentials Provider (8082) e Merchant Payment Processor (8083) só são
acessíveis dentro do container.

Frontend: https://ap2-homolog-frontend.vercel.app
