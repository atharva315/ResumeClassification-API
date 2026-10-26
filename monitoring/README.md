# Prometheus and Grafana monitoring

FastAPI exposes Prometheus-format metrics at `/metrics`. In the current deployment, Prometheus scrapes the API every 15 seconds and Grafana queries Prometheus to display service metrics.

## Prometheus configurations

- `prometheus/aws/prometheus.yml` — target `api:8000` on the shared Docker network, with job name `resume-api`.
- `prometheus/local/prometheus.yml` — target `host.docker.internal:8000` when the API is running on the host and Prometheus runs in Docker Desktop.

These targets represent different network layouts: the EC2 configuration reaches the API by Docker service name, while the local configuration reaches a host process.

## Deployed monitoring topology

- API container: `api`, internal port 8000.
- Prometheus container: `prometheus`, internal port 9090.
- Grafana container: `grafana`, host port 3000 restricted by the EC2 security group.
- UI container: `ui`, public demo port 8501.

The final deployment check showed the `resume-api` target as `up` with no scrape error. Grafana displayed an API availability value of `1` and a request-rate graph showed activity following a test prediction.

The live Prometheus data and Grafana state reside on the EC2 instance. Runtime time-series data and Grafana database files are not part of this repository.
