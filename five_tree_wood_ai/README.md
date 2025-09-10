# Home Assistant Add-on: Five Tree Wood AI

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

_AI-powered aircon temperature prediction for Home Assistant._

## About

Five Tree Wood AI is a Home Assistant add-on that provides intelligent temperature prediction for air conditioning systems using machine learning. It analyzes historical temperature data from InfluxDB to predict future indoor temperatures, helping optimize energy usage and comfort.

## Installation

1. Add this repository to your Home Assistant Supervisor add-on store
2. Install the "Five Tree Wood AI" add-on
3. Configure the add-on (see Configuration section)
4. Start the add-on

## Configuration

```yaml
influxdb_url: "http://influxdb.ninjateaparty:8086"
influxdb_token: "your-influxdb-token"
influxdb_org: "Ninjateaparty"
influxdb_bucket: "homeassistant"
log_level: "info"
api_port: 8099
```

## Usage

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

## Support

Create an issue on the [GitHub repository][github] for support.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[github]: https://github.com/Swamp-Ig/five-tree-wood-ai
