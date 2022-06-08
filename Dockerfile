FROM python:3.10-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13

WORKDIR /app

RUN apt-get update && apt-get upgrade \
    && apt-get -y --no-install-recommends install \
      build-essential=12.9 \
    && pip install --no-cache-dir poetry==$POETRY_VERSION \
    && python -m venv /venv

COPY pyproject.toml ./
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN poetry lock \
    && poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"
COPY docker-entrypoint.sh ./
CMD ["./docker-entrypoint.sh"]
