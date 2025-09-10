# Home Assistant Add-on: Five Tree Wood AI

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

_AI-powered aircon temperature prediction for Home Assistant._

## About

Five Tree Wood AI is a Home Assistant add-on that provides intelligent temperature prediction for air conditioning systems using machine learning. It analyzes historical temperature data from InfluxDB to predict future indoor temperatures, helping optimize energy usage and comfort.

## Features

- **Machine Learning Prediction**: Uses Random Forest Regressor to predict indoor temperatures
- **InfluxDB Integration**: Reads historical temperature data from your Home Assistant InfluxDB
- **REST API**: Provides HTTP endpoints for predictions and model management
- **Automatic Training**: Trains the model automatically on first run
- **Real-time Predictions**: Make temperature predictions via HTTP API
- **Health Monitoring**: Built-in health checks for monitoring

## Installation

1. Add this repository to your Home Assistant Supervisor add-on store
2. Install the "Five Tree Wood AI" add-on
3. Configure the add-on (see Configuration section)
4. Start the add-on

## Configuration

### Add-on configuration:

```yaml
influxdb_url: "http://homeassistant.local:8086"
influxdb_token: "your-influxdb-token"
influxdb_org: "homeassistant"
influxdb_bucket: "homeassistant"
log_level: "info"
api_port: 8099
```

### Option: `influxdb_url`

The URL of your InfluxDB instance. This should be the full URL including protocol and port.

### Option: `influxdb_token` (required)

Your InfluxDB access token. This token needs read access to the specified bucket.

### Option: `influxdb_org`

The InfluxDB organization name (default: "homeassistant").

### Option: `influxdb_bucket`

The InfluxDB bucket containing your Home Assistant data (default: "homeassistant").

### Option: `log_level`

Controls the level of log output. Options: `trace`, `debug`, `info`, `notice`, `warning`, `error`, `fatal`.

### Option: `api_port`

The port on which the REST API will be available (default: 8099).

## Usage

### Training the Model

The model will automatically train on first startup using the last 3 years of data from InfluxDB. You can also manually trigger training:

```bash
curl -X POST http://homeassistant.local:8099/train
```

### Making Predictions

Use the REST API to make temperature predictions:

```bash
curl -X POST http://homeassistant.local:8099/predict \
  -H "Content-Type: application/json" \
  -d '{
    "time": "now",
    "inside_temperature": 22.5,
    "outside_temperature": 15.0,
    "roof_temperature": 18.0,
    "carine_temp_max_0": 20.0,
    "carine_temp_min_1": 12.0
  }'
```

### API Endpoints

- `GET /health` - Health check
- `GET /info` - Model information
- `POST /predict` - Make temperature prediction
- `POST /train` - Retrain the model

## Required Entities

The add-on expects the following entities to be available in InfluxDB:

- `inside_temperature` - Indoor temperature sensor
- `outside_temperature` - Outdoor temperature sensor
- `roof_temperature` - Roof temperature sensor
- `carine_temp_max_0` - Daily maximum temperature forecast
- `carine_temp_min_1` - Next day minimum temperature forecast
- `controller` - Aircon controller state (on/off)

## Data Requirements

For optimal performance, the add-on requires:

- At least several months of historical data
- Regular data collection (recommended: every 15 minutes)
- Consistent entity naming in Home Assistant

## Troubleshooting

### Model Training Issues

If model training fails:

1. Check InfluxDB connectivity and credentials
2. Verify required entities exist in InfluxDB
3. Ensure sufficient historical data (recommended: 3+ months)
4. Check logs for specific error messages

### API Issues

If the API is not responding:

1. Verify the add-on is running
2. Check port configuration
3. Review add-on logs for errors

## Support

Create an issue on the [GitHub repository][github] for support.

## License

MIT License - see the [LICENSE](LICENSE) file for details.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[github]: https://github.com/pennyw00d/five-tree-wood-ai
