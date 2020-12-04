FROM python:alpine3.12

WORKDIR /usr/src

COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache --virtual build-dependencies \
      build-base==0.5-r2 \
      libffi-dev==3.3-r2 \
      openssl-dev==1.1.1g-r0 \
    && apk add --no-cache \
      supervisor==4.2.0-r0 \
    && pip3 install -r /tmp/requirements.txt \
    && apk del build-dependencies

COPY ecowitt2mqtt /usr/src/ecowitt2mqtt
COPY supervisord.conf /etc/supervisord.conf
COPY run.sh /usr/local/bin/run.sh

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/ecowitt2mqtt"

ENTRYPOINT ["/usr/local/bin/run.sh"]
