########################################################################################
# Stage 1: Dependency Builder
#
# This stage is responsible for building the dependencies.
########################################################################################
FROM python:3.9-alpine as builder
ARG TARGETPLATFORM

# Set up the build environment:
ENV CRYPTOGRAPHY_VERSION=40.0.1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1 \
    POETRY_VERSION=1.4.2 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add base libraries:
SHELL ["/bin/ash", "-o", "pipefail", "-c"]
RUN apk add --no-cache \
      bash \
      build-base \
      libffi-dev \
      python3-dev

# Add poetry and build dependencies:
COPY . .
RUN printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf \
    && pip install --upgrade pip \
    && pip install cryptography==${CRYPTOGRAPHY_VERSION} \
    && pip install poetry==${POETRY_VERSION} \
    && python3 -m venv /venv
RUN poetry export --without-hashes -f requirements.txt \
       | /venv/bin/pip install -r /dev/stdin \
   && poetry build \
   && /venv/bin/pip install dist/*.whl

########################################################################################
# Stage 2: Final
#
# This stage is responsible for building the final image.
########################################################################################
FROM python:3.9-alpine as final
ARG TARGETPLATFORM

# Copy the virtual environment from the builder image:
COPY --from=builder /venv /venv
ENV VIRTUAL_ENV="/venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Add ecowitt2mqtt user and group:
RUN addgroup --gid 1000 ecowitt2mqtt && adduser --uid 1000 --gid 1000 ecowitt2mqtt
RUN chown -R ecowitt2mqtt:ecowitt2mqtt ${VIRTUAL_ENV}
USER 1000

CMD ["ecowitt2mqtt"]
