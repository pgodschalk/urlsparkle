FROM python:3.13 AS build

ENV PATH=/home/worker/.venv/bin:$PATH \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PROJECT_ENVIRONMENT=/home/worker/.venv \
  VIRTUAL_ENV=/home/worker/.venv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /home/worker

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev



FROM python:3.13-slim-bookworm AS production

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
  --mount=target=/var/cache/apt,type=cache,sharing=locked \
  apt-get update && \
  apt-get -y --no-install-recommends install \
  curl

RUN useradd -m worker
RUN mkdir -p /home/worker/.cache/uv
RUN chown -R worker:worker /home/worker/.cache/uv
USER worker

ENV PATH=/home/worker/.venv/bin:$PATH \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PROJECT_ENVIRONMENT=/home/worker/.venv \
  VIRTUAL_ENV=/home/worker/.venv

WORKDIR /home/worker

COPY --from=build /home/worker/.venv /home/worker/.venv

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD ["curl", "-I",  "--fail", "http://localhost:8080/healthz"]



FROM production AS development

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --from=build /home/worker/.venv /home/worker/.venv

USER root
RUN chown -R worker:worker /home/worker/.venv
USER worker

COPY --chown=worker:worker . .

RUN uv sync --frozen

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
