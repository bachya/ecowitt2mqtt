# Define the builder image:
FROM python:3.11 as builder
ARG TARGETPLATFORM
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add base libraries (mostly for building cryptography):
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      libffi-dev \
      libssl-dev \
      pkg-config \
      python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Add rust:
ENV PATH="${HOME}/.cargo/bin:${PATH}"
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y \
    && rustup toolchain install nightly

# Add poetry and build dependencies:
COPY . .
RUN printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install cryptography==40.0.1 \
    && python3 -m pip install poetry==1.4.2 \
    && python3 -m venv /venv
RUN poetry lock \
    && poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin \
   && poetry build \
   && /venv/bin/python3 -m pip install dist/*.whl

# Define the final image:
FROM python:3.11-slim as final
ARG TARGETPLATFORM

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set up s6-overlay:
COPY ./s6/rootfs /
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      tar \
      xz-utils \
    && case ${TARGETPLATFORM} in \
         "linux/386")    S6_ARCH=i686  ;; \
         "linux/amd64")  S6_ARCH=x86_64  ;; \
         "linux/arm/v6") S6_ARCH=arm  ;; \
         "linux/arm/v7") S6_ARCH=arm  ;; \
         "linux/arm64")  S6_ARCH=aarch64  ;; \
       esac \
    && S6_VERSION="3.1.2.1" \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-noarch.tar.xz" \
        | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
        | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-symlinks-noarch.tar.xz" \
        | tar -C / -Jxpf - \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_VERSION}/s6-overlay-symlinks-arch.tar.xz" \
        | tar -C / -Jxpf - \
    && apt-get remove -y \
      xz-utils \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Add ecowitt2mqtt user and group:
RUN addgroup --gid 1000 ecowitt2mqtt && adduser --uid 1000 --gid 1000 ecowitt2mqtt
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV}
USER 1000

ENTRYPOINT ["/init"]
