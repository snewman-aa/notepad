FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
LABEL authors="snewman"

ADD . /app

WORKDIR /app
RUN uv sync --frozen

EXPOSE 5050

CMD ["uv", "run", "run.py"]