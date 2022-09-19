FROM python:3.10-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# hadolint ignore=DL3018
RUN apk add --no-cache \
        bash \
        build-base \
        gcc \
        libffi-dev \
        musl-dev \
        openssl-dev \
        python3-dev

RUN \
    if [ "$(uname -m)" = "armv7l" ]; then \
        printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf ; \
    fi

# hadolint ignore=DL3013
RUN python3 -m pip install \
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
RUN addgroup -g 1000 -S ecowitt2mqtt \
    && adduser -u 1000 -S ecowitt2mqtt -G ecowitt2mqtt
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"
COPY docker-entrypoint.sh /usr/local/bin/
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV} /app /usr/local/bin/docker-entrypoint.sh
USER 1000
ENTRYPOINT ["docker-entrypoint.sh"]
