## Como executar os testes:

Execute a partir da raiz do repositório:

```bash
# Remove o ambiente virtual quebrado
rm -rf .venv

# Opcional: limpa o cache do uv para garantir wheels novas
uv cache clean

# Recria o ambiente e executa os testes
uv sync
uv run python -m pytest code/sdk/python/ap2/tests/ -v
```