FROM python:alpine3.12

WORKDIR /usr/src

COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache --virtual build-dependencies \
      build-base==0.5-r2 \
      libffi-dev==3.3-r2 \
    && apk add --no-cache \
      bash==5.0.17-r0 \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && apk del build-dependencies

COPY ecowitt2mqtt /usr/src/ecowitt2mqtt
COPY run.sh /usr/local/bin/run.sh

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/ecowitt2mqtt"

CMD ["/usr/local/bin/run.sh"]
