FROM python:alpine3.12

COPY ecowitt2mqtt /usr/src/app
COPY requirements.txt /usr/src/app

RUN apk add --no-cache --virtual build-dependencies \
    && pip install -r /usr/src/app/requirements.txt \
    && apk del build-dependencies

# Copy configuration files:
COPY supervisord.conf /etc/supervisord.conf
COPY run.sh /usr/local/bin/run.sh

# Run:
ENTRYPOINT ["/usr/local/bin/run.sh"]
