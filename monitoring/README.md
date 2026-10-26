# Prometheus and Grafana monitoring

The API exposes Prometheus-format metrics at `/metrics`. Keep this endpoint reachable only by trusted monitoring components; do not publish it directly to the public internet.

## Configuration files

- `prometheus/aws/prometheus.yml`: scrape target `api:8000`, for Prometheus on the same Docker network as the API. The job name is `resume-api`.
- `prometheus/local/prometheus.yml`: target `host.docker.internal:8000`, for Docker Desktop when the API is running directly on the Windows host.

Do not interchange these configurations without checking where the API runs.

## Current EC2 deployment

The tested instance runs these containers on Docker network `resume-net`:

- `api` — FastAPI, internal port 8000
- `prometheus` — scrapes `http://api:8000/metrics` every 15 seconds
- `grafana` — reads metrics from Prometheus

Prometheus port 9090 is not host-published. Grafana host port 3000 is restricted by the EC2 security group to the administrator's current IP. The public Streamlit demo uses host port 8501; the API should remain private.

The live Prometheus configuration and data volume on EC2 are active. Committing a config file here does not remotely change the instance. Apply changes to EC2 only through a deliberate deployment step.

## Local monitoring

The local-only Compose file is `../deploy/local/docker-compose.monitoring.yml`. It binds monitoring ports to `127.0.0.1`; set `GRAFANA_ADMIN_PASSWORD` in the environment before starting it. Do not use a default password or expose these ports publicly.

## Dashboard export

The Grafana dashboards currently live in the EC2 Grafana data volume and were created in the Grafana UI. The source archive did not include dashboard JSON or provisioning files. To version dashboards, export JSON from the Grafana UI and commit it under `monitoring/grafana/dashboards/` after reviewing the export for credentials or sensitive URLs.

Never commit Grafana databases, Prometheus time-series data, credentials, or resume content.
