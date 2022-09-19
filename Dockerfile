FROM python:3.10-slim-bullseye as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev

RUN \
    if [ "$(uname -m)" = "armv7l" ]; then \
        printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf ; \
    fi

# hadolint ignore=DL3013
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install poetry \
    && python3 -m venv /venv
COPY pyproject.toml ./
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN poetry lock && poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin
COPY . .
RUN poetry build && /venv/bin/python3 -m pip install dist/*.whl

FROM base as final
WORKDIR /app
RUN groupadd -g 1000 ecowitt2mqtt \
    && useradd ecowitt2mqtt -u 1000 -g 1000
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"
COPY docker-entrypoint.sh /usr/local/bin/
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV} /app /usr/local/bin/docker-entrypoint.sh
USER 1000
ENTRYPOINT ["docker-entrypoint.sh"]
