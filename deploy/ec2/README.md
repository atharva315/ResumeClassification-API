# AWS EC2 deployment record

The deployed application was tested on Amazon EC2 in Sydney (`ap-southeast-2`) using Amazon Linux 2023. This document records the verified container topology and includes a Compose definition for reproducible reference. The original running containers were created with `docker run`; the Compose file has not been applied to the existing instance.

## Runtime topology

| Container | Image / service | Exposure |
|---|---|---|
| `ui` | `rockstar1505/resumeclassification-ui` | Host TCP 8501 |
| `api` | `rockstar1505/resume-classification-api` | Internal Docker TCP 8000 |
| `prometheus` | `prom/prometheus` | Internal Docker TCP 9090 |
| `grafana` | `grafana/grafana` | Host TCP 3000; restricted by the EC2 security group |

The services use Docker network `resume-net`. The UI uses `API_BASE_URL=http://api:8000`; Prometheus scrapes `http://api:8000/metrics`. The API and Prometheus ports are not publicly published. The Streamlit page was tested through the public host port, and Grafana access was restricted to the administrator's IP.

## Last observed verification

During the deployment session, all four containers were running. Prometheus reported the `resume-api` target as `up` with no scrape error. A test resume submission returned a prediction in Streamlit. Grafana displayed `API Availability = 1` and the request-rate graph showed activity.

The instance was subsequently stopped to reduce compute costs. This repository does not claim that EC2 is currently online. EBS storage and other attached resources may still incur charges while stopped, and an automatically assigned public IPv4 address may change on restart.

## Compose definition

`docker-compose.yml` records the four-service layout and pins the API and UI to the same Docker Hub image digests used in the tested deployment. Prometheus and Grafana use their public image tags.

The Compose definition uses an external network named `resume-net` and external named volumes `prometheus-data` and `grafana-data`. Before applying it to an existing EC2 host, compare the live container mounts with those names:

~~~bash
sudo docker inspect -f '{{range .Mounts}}{{println .Name .Destination .Source}}{{end}}' prometheus grafana
sudo docker inspect -f '{{json .NetworkSettings.Networks}}' api ui prometheus grafana
~~~

The live containers were created outside Compose. Compose cannot automatically adopt those existing container objects. Do not run `docker compose up` against the existing host as a routine step: container-name conflicts or a different volume mapping could interrupt services or make the current Grafana state appear missing. The Compose file is suitable as a reproducible definition for a fresh deployment or a planned, validated migration after the current mounts are confirmed.

## Fresh-instance prerequisites

- Amazon Linux 2023 or another supported Linux host with Docker Engine and the Docker Compose plugin.
- Outbound network access to pull public Docker Hub images.
- Security group allowing TCP 8501 for the public demo; SSH 22 only from the required administration sources; TCP 3000 only from the administrator's IP.
- No public inbound rule for TCP 8000 or 9090.
- A strong Grafana admin password kept in the local `deploy/ec2/.env` file, which must not be committed.

## Fresh-instance launch

From a checkout of this repository on a new/clean host, create the external Docker network and volumes, configure the local Grafana password, and validate the Compose configuration before starting services:

~~~bash
sudo docker network create resume-net
sudo docker volume create prometheus-data
sudo docker volume create grafana-data
cp deploy/ec2/.env.example deploy/ec2/.env
# Edit deploy/ec2/.env and replace the example password before launch.
sudo docker compose --env-file deploy/ec2/.env -f deploy/ec2/docker-compose.yml config
sudo docker compose --env-file deploy/ec2/.env -f deploy/ec2/docker-compose.yml pull
sudo docker compose --env-file deploy/ec2/.env -f deploy/ec2/docker-compose.yml up -d
sudo docker compose --env-file deploy/ec2/.env -f deploy/ec2/docker-compose.yml ps
~~~

These are fresh-instance commands, not commands to execute on the existing host without checking its mounts and network first. The API and UI use immutable Docker Hub digests to match the tested image versions. A fresh checkout needs Git LFS for the source model artifact, but the runtime Compose file pulls the prebuilt API image and does not build it locally.

## Health and monitoring checks

~~~bash
sudo docker ps
sudo docker exec api python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5).read().decode())"
sudo docker exec api python -c "import json,urllib.request; d=json.load(urllib.request.urlopen('http://prometheus:9090/api/v1/targets')); print([(t['labels'].get('job'),t['health'],t.get('lastError')) for t in d['data']['activeTargets']])"
~~~

Open `http://<EC2-Public-IP>:8501` for Streamlit. Grafana is at `http://<EC2-Public-IP>:3000` only when the security group permits the administrator's current public IP. These checks should be observed after any intentional deployment or restart; historical results do not guarantee current uptime.

## Port, storage and cost notes

- TCP 8501: public Streamlit demo.
- TCP 8000: private API service.
- TCP 9090: private Prometheus service.
- TCP 3000: Grafana, restricted to the administrator's IP by the security group.
- Preserve `grafana-data` and `prometheus-data`; do not delete monitoring volumes as part of routine container updates.
- To save compute cost after a demo, use **EC2 → Instance state → Stop instance**, not Terminate. Containers and monitoring are offline while the instance is stopped. EBS storage and other associated resources may continue to incur charges; the public IPv4 address may change after a subsequent start.

## Why the earlier Caddy/DuckDNS bundle is not used

The earlier `docker-compose.aws.yml` in the separate deployment bundle expects ECR environment variables, introduces another network, and adds Caddy plus a DuckDNS updater. Those services are not part of this verified deployment.
