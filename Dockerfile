FROM python:3.10-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
# hadolint ignore=DL3018,DL3013
RUN apk add --no-cache \
        bash \
        build-base \
        cargo \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev \
        python3-dev \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install \
        cryptography \
        poetry \
    && python3 -m venv /venv
COPY pyproject.toml ./
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN poetry lock && poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin
COPY . .
RUN poetry build && /venv/bin/python3 -m pip install dist/*.whl

FROM base as final
WORKDIR /app
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"
COPY docker-entrypoint.sh ./
CMD ["./docker-entrypoint.sh"]
