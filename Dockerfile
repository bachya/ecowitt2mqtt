FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install poetry and dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY ecowitt2mqtt/ ./ecowitt2mqtt/

# Create config directory
RUN mkdir -p /config

# Set environment variables
ENV CONFIG_DIR=/config
ENV PYTHONUNBUFFERED=1

# Expose default port
EXPOSE 8080

# Volume for persistent config
VOLUME ["/config"]

# Run the application
CMD ["python", "-m", "ecowitt2mqtt"]
