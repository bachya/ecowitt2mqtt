FROM python:3.10-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
# hadolint ignore=DL3013
RUN apk add --no-cache \
        bash==5.1.16-r2 \
        build-base==0.5-r3 \
        cargo==1.60.0-r2 \
        gcc==11.2.1_git20220219-r2 \
        libffi-dev==3.4.2-r1 \
        musl-dev==1.2.3-r0 \
        openssl-dev==1.1.1o-r0 \
        python3-dev==3.10.4-r0 \
    && python3 -m pip install --upgrade \
        cryptography==37.0.2 \
        pip \
        poetry==1.1.13 \
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
