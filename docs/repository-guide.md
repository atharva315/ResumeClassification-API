# Repository guide

This repository is the source and operations record for the deployed ModernBERT ResumeClassification application.

## Application source

- `services/api/app.py` — FastAPI routes, model loading, prediction preprocessing, file extraction and Prometheus metrics.
- `services/api/Dockerfile` — API runtime image definition, including Tesseract OCR and the local model directory.
- `services/api/requirements.txt` — API runtime dependencies.
- `services/api/requirements-dev.txt` — test dependencies on top of runtime dependencies.
- `services/api/tests/test_api.py` — API regression tests that mock model inference and exercise routes and extraction behavior.
- `services/api/scripts/diagnose_image_ocr.py` — local diagnostic utility for inspecting OCR quality; it may write extracted text, so generated diagnostic files should be kept private.
- `services/api/model_manifest.json` — model architecture, label count, token limit and recorded evaluation metrics.
- `services/api/model/README.md` — required model artifact inventory and the current checkpoint availability note.

- `services/frontend/streamlit_app.py` — UI for text input and resume file upload; calls the API rather than loading a model in the UI process.
- `services/frontend/Dockerfile` and `requirements.txt` — UI image and dependencies.

## Deployment and monitoring

- `deploy/local/docker-compose.local.yml` — local UI container for a FastAPI service running directly on the host.
- `deploy/local/docker-compose.monitoring.yml` — optional local Prometheus/Grafana services, bound to loopback.
- `deploy/ec2/README.md` — documents the four containers currently running on EC2 and rules for safe updates.
- `monitoring/prometheus/aws/prometheus.yml` — Prometheus scrape target on the shared Docker network, `api:8000`.
- `monitoring/prometheus/local/prometheus.yml` — Prometheus target when the API runs on the host and Prometheus runs in Docker Desktop.
- `monitoring/grafana/README.md` — how to export and version dashboards. The live dashboards remain in the existing Grafana volume until exported.
- `docs/architecture.md` — component and network map.
- `docs/cicd-roadmap.md` and `.github/workflows/README.md` — gated CI/CD plan; no publish or deployment workflow is active yet.

## Files intentionally excluded

The repository does not contain the full training dataset, individual resume records, generated prediction logs, the full Grafana database, Prometheus time-series data, backups, Python caches, AWS credentials, or real environment files. The model weights are also not committed yet; this is the remaining dependency for rebuilding the API image from source.

See the root README and model-development notes before using any deployment configuration. The alternate Caddy/DuckDNS Compose file from the earlier deployment bundle is not part of the current runtime and must not be launched against the existing EC2 instance.
