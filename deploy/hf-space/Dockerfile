# Backend de homologação do AP2 para Hugging Face Spaces (SDK: docker).
# Este mesmo arquivo é o Dockerfile do Space ds-fabiopinheiro/ap2-homolog-backend:
# ele clona o branch homolog-deploy do GitHub e sobe os papéis com start.sh.
FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git nginx curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv==0.8.17

# O HF Spaces executa o container com UID 1000.
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

ARG AP2_OWNER_REPO=ds-fabiopinheiro/ap2-protocol
ARG AP2_REF=homolog-deploy
# Disponível em tempo de execução para o start.sh registrar o branch clonado.
ENV AP2_REF=${AP2_REF}
# O conteúdo desta URL muda a cada commit no branch, o que invalida o cache
# do Docker e força um clone novo no rebuild do Space.
ADD https://api.github.com/repos/${AP2_OWNER_REPO}/commits/${AP2_REF} /tmp/ap2-ref.json
RUN git clone --depth 1 --branch "${AP2_REF}" "https://github.com/${AP2_OWNER_REPO}.git" /app \
 && chown -R user:user /app

USER user
WORKDIR /app
RUN uv sync --package ap2-samples

EXPOSE 7860
CMD ["bash", "deploy/hf-space/start.sh"]
