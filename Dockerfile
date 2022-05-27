FROM python:alpine3.16 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13

WORKDIR /app

RUN apk add --no-cache \
      bash==5.1.16-r2 \
      build-base==0.5-r2 \
      libffi-dev==3.4.2-r1 \
    && pip install --no-cache-dir poetry==$POETRY_VERSION \
    && python -m venv /venv

COPY pyproject.toml poetry.lock ./
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN poetry export --without-hashes -f requirements.txt \
    | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

WORKDIR /app

RUN apk add --no-cache \
      build-base==0.5-r2 \
      libffi-dev==3.4.2-r1
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"
COPY docker-entrypoint.sh ./
CMD ["./docker-entrypoint.sh"]
