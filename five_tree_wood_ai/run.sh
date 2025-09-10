#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Five Tree Wood AI
# Runs the Five Tree Wood AI temperature prediction service
# ==============================================================================

# Get configuration
CONFIG_PATH="/data/options.json"
INFLUXDB_URL=$(bashio::config 'influxdb_url')
INFLUXDB_TOKEN=$(bashio::config 'influxdb_token')
INFLUXDB_ORG=$(bashio::config 'influxdb_org')
INFLUXDB_BUCKET=$(bashio::config 'influxdb_bucket' 'homeassistant')
LOG_LEVEL=$(bashio::config 'log_level' 'info')
API_PORT=$(bashio::config 'api_port' '8099')

# Set log level
bashio::log.level "${LOG_LEVEL}"

bashio::log.info "Starting Five Tree Wood AI..."
bashio::log.info "InfluxDB URL: ${INFLUXDB_URL}"
bashio::log.info "InfluxDB Org: ${INFLUXDB_ORG}"
bashio::log.info "InfluxDB Bucket: ${INFLUXDB_BUCKET}"
bashio::log.info "API Port: ${API_PORT}"

# Create configuration directory
mkdir -p /data/conf

# Create configuration files
cat > /data/conf/config.ini << EOF
[influxdb]
url = ${INFLUXDB_URL}
org = ${INFLUXDB_ORG}
bucket = ${INFLUXDB_BUCKET}

[api]
port = ${API_PORT}
host = 0.0.0.0
EOF

cat > /data/conf/secrets.ini << EOF
[influxdb]
token = ${INFLUXDB_TOKEN}
EOF

# Set configuration directory
export FIVTREEWD_CONFIG_DIR="/data/conf"

# Check if model exists, if not train it
if [ ! -f "/data/conf/aircon_model.pkl" ]; then
    bashio::log.info "No trained model found. Training initial model..."
    cd /app && python src/main.py -C /data/conf train
fi

# Start the API server
bashio::log.info "Starting Five Tree Wood AI REST API on port ${API_PORT}..."
cd /app && exec python src/main.py -C /data/conf api --host 0.0.0.0 --port "${API_PORT}"
