ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:13.1.2
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy Python requirements
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN \
    apk add --no-cache --virtual .build-dependencies \
    build-base \
    libffi-dev \
    openssl-dev \
    cargo \
    rust \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del --no-cache .build-dependencies \
    && rm -rf /var/cache/apk/* \
    && rm -f /tmp/requirements.txt

# Copy application
COPY src/ /app/src/
COPY pyproject.toml /app/

# Install the package
WORKDIR /app
RUN pip install --no-cache-dir -e .

# Copy run script
COPY run.sh /
RUN chmod a+x /run.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:8099/health || exit 1

# Labels
LABEL \
    io.hass.name="Five Tree Wood AI" \
    io.hass.description="AI-powered aircon temperature prediction" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Penny Wood <github@ninjateaparty.com>" \
    org.opencontainers.image.title="Five Tree Wood AI" \
    org.opencontainers.image.description="AI-powered aircon temperature prediction for Home Assistant" \
    org.opencontainers.image.vendor="Five Tree Wood" \
    org.opencontainers.image.authors="Penny Wood <github@ninjateaparty.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/pennyw00d/five-tree-wood-ai" \
    org.opencontainers.image.source="https://github.com/pennyw00d/five-tree-wood-ai" \
    org.opencontainers.image.documentation="https://github.com/pennyw00d/five-tree-wood-ai/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}

# Run
CMD [ "/run.sh" ]
