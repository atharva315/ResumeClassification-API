# Existing AWS EC2 deployment

This document records the working deployment configuration from the verified deployment session. It is documentation only; it does not recreate or alter EC2 infrastructure.

## Environment

- Region: `ap-southeast-2` (Sydney).
- EC2 instance: `ResumeClassificationDemo` (`i-013c63daf6fae128e`).
- Docker network: `resume-net`.
- Docker Hub API image: `rockstar1505/resume-classification-api:latest`.
- Docker Hub UI image: `rockstar1505/resumeclassification-ui:latest`.
- Containers: `api`, `ui`, `prometheus`, and `grafana`.

## Port and network policy

- Streamlit UI: host TCP 8501, intended to be public for the demo.
- API: container TCP 8000, available on the Docker network; do not add a public host mapping.
- Prometheus: container TCP 9090, internal only.
- Grafana: host TCP 3000, restrict the EC2 security-group source to the administrator's current public IP.
- SSH (22): keep restricted to the configured administrator/AWS access sources.

The UI uses `API_BASE_URL=http://api:8000`, so `ui` and `api` must share `resume-net`. Prometheus scrapes `http://api:8000/metrics`.

## Existing container commands

The current deployment was created using `docker run`, not the Compose file included in the earlier experimental bundle. Previously used equivalent commands were:

```bash
sudo docker network create resume-net 2>/dev/null || true
sudo docker run -d --name api --network resume-net --restart unless-stopped rockstar1505/resume-classification-api:latest
sudo docker run -d --name ui --network resume-net --restart unless-stopped -p 8501:8501 rockstar1505/resumeclassification-ui:latest
```

These are initial deployment examples, not commands to repeat against an already-running host. Before updating an existing service, pull and validate the new image tag first, save the known-good image tag for rollback, then replace only that app container. Never remove `prometheus` or `grafana` or their named data volumes as part of UI/API deployment.

Prometheus and Grafana were added separately with persistent volumes and `--restart unless-stopped`; preserve their current configuration and data. The EC2 instance may be stopped after demonstrations to reduce compute costs. The app and monitoring are offline while stopped; EBS and other associated resources may still incur charges. The public IP can change after restart.

## Why the experimental AWS Compose is not used

The earlier `docker-compose.aws.yml` expects ECR variables, introduces a different `appnet` network, and adds Caddy plus a DuckDNS updater. Those services are not part of the verified live deployment. Do not run that Compose file on the existing host without an intentional, tested migration.
