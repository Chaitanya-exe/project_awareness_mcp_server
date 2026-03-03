FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

ENV DATABASE_URL="postgresql+psycopg://mcp_user:mcp_pass1234@localhost:5432/mcp_server"

EXPOSE 8000

CMD ["uv", "run", "mcpo", "--host", "0.0.0.0", "--port", "8000", "--", "uv", "run", "main.py"]