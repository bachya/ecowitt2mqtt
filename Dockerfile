FROM python:alpine3.12

COPY ecowitt2mqtt /usr/src/app

RUN apk add --no-cache --virtual build-dependencies \
      build-base==0.5-r2 \
      libffi-dev==3.3-r2 \
      openssl-dev==1.1.1g-r0 \
    && apk add --no-cache \
      openssl==1.1.1g-r0 \
    && pip install \
      aiohttp==3.6.2 \
      asyncio-mqtt==0.7.0 \
      supervisor==4.2.1 \
    && apk del build-dependencies

# Copy configuration files:
COPY supervisord.conf /etc/supervisord.conf
COPY run.sh /usr/local/bin/run.sh

# Run:
ENTRYPOINT ["/usr/local/bin/run.sh"]
