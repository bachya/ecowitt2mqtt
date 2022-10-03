FROM python:3.9.14-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apk add --no-cache \
    bash==5.1.16-r2 \
    build-base==0.5-r3 \
    libffi-dev==3.4.2-r1 \
    musl-dev==1.2.3-r0 \
    openssl-dev==1.1.1q-r0 \
    python3-dev==3.10.5-r0
# hadolint ignore=DL3013
RUN printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf \
    && pip install --upgrade pip \
    && python3 -m pip install cryptography==38.0.1 \
    && python3 -m pip install poetry==1.2.1 \
    && python3 -m venv /venv
COPY pyproject.toml ./
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN poetry lock && poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin
COPY . .
RUN poetry build && /venv/bin/python3 -m pip install dist/*.whl

FROM base as final
WORKDIR /app
RUN addgroup -g 1000 -S ecowitt2mqtt \
    && adduser -u 1000 -S ecowitt2mqtt -G ecowitt2mqtt
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"
COPY docker-entrypoint.sh /usr/local/bin/
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV} /app /usr/local/bin/docker-entrypoint.sh
USER 1000
ENTRYPOINT ["docker-entrypoint.sh"]
