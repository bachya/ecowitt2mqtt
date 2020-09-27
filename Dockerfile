FROM python:alpine3.12

COPY README.md /usr/src/README.md
COPY ecowitt2mqtt /usr/src/ecowitt2mqtt
COPY pyproject.toml /usr/src/pyproject.toml

WORKDIR /usr/src

RUN apk add --no-cache --virtual build-dependencies \
      build-base==0.5-r2 \
      libffi-dev==3.3-r2 \
      openssl-dev==1.1.1g-r0 \
    && apk add --no-cache \
      supervisor==4.2.0-r0 \
    && pip3 install poetry==1.0.10 \
    && poetry config virtualenvs.create false \
    && poetry lock && poetry install --no-dev \
    && pip3 uninstall -y poetry \
    && apk del build-dependencies

# Copy configuration files:
COPY supervisord.conf /etc/supervisord.conf
COPY run.sh /usr/local/bin/run.sh

# Run:
ENTRYPOINT ["/usr/local/bin/run.sh"]
