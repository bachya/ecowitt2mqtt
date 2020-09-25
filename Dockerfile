FROM python:alpine3.12

COPY ecowitt2mqtt /usr/src/app

# hadolint ignore=DL3003
RUN apk add --no-cache --virtual build-dependencies \
      build-base \
      libffi-dev \
      openssl-dev \
    && apk add --no-cache \
      openssl \
    && pip install \
      aiohttp \
      asyncio-mqtt \
      supervisor \
    && apk del build-dependencies

# Copy configuration files:
COPY supervisord.conf /etc/supervisord.conf
COPY run.sh /usr/local/bin/run.sh

# Run:
ENTRYPOINT ["/usr/local/bin/run.sh"]
