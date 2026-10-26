# AWS EC2 deployment record

The application and monitoring stack has been deployed and verified on Amazon EC2. This file records the completed environment and the observed runtime layout.

## Environment

- AWS region: `ap-southeast-2` (Sydney)
- Operating system: Amazon Linux 2023
- Instance name: `ResumeClassificationDemo`
- Docker network: `resume-net`
- Image registry: Docker Hub
- API image: `rockstar1505/resume-classification-api:latest`
- UI image: `rockstar1505/resumeclassification-ui:latest`

## Running services

| Container | Service | Exposure |
|---|---|---|
| `ui` | Streamlit frontend | Host TCP 8501 |
| `api` | FastAPI inference service | Container TCP 8000 on `resume-net` |
| `prometheus` | API metrics collection | Container TCP 9090 on the Docker network |
| `grafana` | Monitoring dashboards | Host TCP 3000, restricted by the EC2 security group |

The UI uses `API_BASE_URL=http://api:8000`. Prometheus scrapes `http://api:8000/metrics`. The API and Prometheus ports are not publicly published. The security group exposes the Streamlit demo and restricts Grafana access to the administrator's public IP.

## Verification record

- All four containers were running in the final container check.
- The Prometheus target `resume-api` reported health `up` with no scrape error.
- A test resume submission returned a classification through the Streamlit interface.
- Grafana displayed `API Availability = 1` and a request-rate graph showed activity after the test request.
- The deployment uses the existing Docker Hub images rather than the experimental Caddy/DuckDNS Compose bundle.

## Operational notes

The UI, API and monitoring are unavailable while EC2 is stopped. The instance's public IPv4 address can change after starting it again. EBS storage and other associated resources may continue to incur charges while the instance is stopped. The AWS budget is an alert rather than a spending cap.
