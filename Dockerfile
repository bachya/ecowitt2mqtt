# Define the base image:
FROM python:3.9.14-alpine as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# Define the builder image:
FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1

WORKDIR /app

SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN apk add --no-cache \
      bash==5.1.16-r2 \
      build-base==0.5-r3 \
      cargo==1.60.0-r2 \
      libffi-dev==3.4.2-r1 \
      musl-dev==1.2.3-r0 \
      openssl-dev==1.1.1q-r0 \
      python3-dev==3.10.5-r0
RUN printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf \
    && python3 -m pip install cryptography==38.0.1 \
    && python3 -m pip install poetry==1.2.1 \
    && python3 -m venv /venv

COPY pyproject.toml ./
RUN poetry lock && poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/python3 -m pip install dist/*.whl

# Define the final image:
FROM base as final
ARG BUILD_ARCH="${TARGETARCH}"

COPY ./s6/rootfs /

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"

SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN apk add --no-cache --virtual .build-dependencies \
      curl==7.83.1-r3 \
      tar==1.34-r0 \
      xz==5.2.5-r1 \
    && case ${BUILD_ARCH} in \
         "linux/amd64")  S6_ARCH=x86_64  ;; \
         "linux/arm/v6") S6_ARCH=arm32  ;; \
         "linux/arm/v7") S6_ARCH=arm32  ;; \
         "linux/arm64")  S6_ARCH=aarch64  ;; \
         "linux/i386")   S6_ARCH=i686  ;; \
       esac \
    && S6_VERSION="3.1.2.1" \
    && echo "AARON" \
    && echo "$RUNNER_ARCH" \
    && echo "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-noarch.tar.xz" \
        | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
        | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-symlinks-noarch.tar.xz" \
        | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-symlinks-arch.tar.xz" \
        | tar -C / -Jxpf - \
    && apk del --no-cache --purge .build-dependencies \
    && rm -f -r /tmp/*

RUN addgroup -g 1000 -S ecowitt2mqtt \
    && adduser -u 1000 -S ecowitt2mqtt -G ecowitt2mqtt
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV}
USER 1000

ENTRYPOINT ["/init"]
