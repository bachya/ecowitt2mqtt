########################################################################################
# Stage 1: Dependency Builder
#
# This stage is responsible for building the ecowitt2mqtt package and its dependencies.
########################################################################################
FROM python:3.11-alpine AS builder
ARG TARGETPLATFORM

# Set up the build environment:
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1 \
    POETRY_VERSION=2.1.2 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Add base libraries:
SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN apk add --no-cache \
      bash \
      build-base \
      libffi-dev \
      python3-dev

# Add poetry and build dependencies:
COPY . .
RUN pip install --upgrade pip \
    && pip install poetry==${POETRY_VERSION} "poetry-plugin-export"\
    && python3 -m venv /venv
RUN poetry export --without-hashes -f requirements.txt --only main \
       | /venv/bin/pip install -r /dev/stdin \
   && poetry build \
   && /venv/bin/pip install dist/*.whl

########################################################################################
# Stage 2: Final
#
# This stage is responsible for building the final image.
########################################################################################
FROM python:3.11-alpine AS final
ARG TARGETPLATFORM

# Copy the virtual environment from the builder image:
COPY --from=builder /venv /venv
ENV VIRTUAL_ENV="/venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# ---- BEGIN: Config volume conventions ----
# Standard location for persistent configuration/state in the container:
ENV CONFIG_DIR="/config" \
    ECOWITT2MQTT_CONFIG="/config/config.yaml"

# Create the directory at build time (so it exists even without a bind mount):
RUN mkdir -p /config

# Declare intent that /config is a volume (Docker will create an anonymous volume
# if the user doesn't bind-mount one):
VOLUME ["/config"]
# ---- END: Config volume conventions ----

# Add ecowitt2mqtt user and group:
RUN addgroup -g 1000 -S ecowitt2mqtt && adduser -u 1000 -S ecowitt2mqtt -G ecowitt2mqtt
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV}
USER 1000

CMD ["ecowitt2mqtt"]
