# Repository guide

This repository contains the source, training record, deployment configuration and monitoring notes for the ModernBERT ResumeClassification application.

## Application source

- `services/api/app.py` — FastAPI routes, model loading, preprocessing, document/image extraction and Prometheus metrics.
- `services/api/Dockerfile` — API image definition, including Tesseract OCR and the expected local model directory.
- `services/api/requirements.txt` — runtime dependencies for the inference service.
- `services/api/requirements-dev.txt` — additional dependencies for API regression tests.
- `services/api/tests/test_api.py` — tests for the API routes and extraction behavior with inference mocked.
- `services/api/scripts/diagnose_image_ocr.py` — diagnostic utility for comparing OCR extraction quality. Diagnostic output can contain extracted resume text and should be kept private.
- `services/api/model_manifest.json` — model architecture, category count, configured context length and recorded test metrics.
- `services/api/model/README.md` — expected trained-model file inventory.

- `services/frontend/streamlit_app.py` — user interface for text input, file upload and prediction display.
- `services/frontend/Dockerfile` and `requirements.txt` — UI container and dependencies.

## Model development

- `notebooks/ResumeClassification_Model_Development.ipynb` — Kaggle notebook covering ResumeAtlas data checks, duplicate/conflicting-label review, split creation, token-length analysis, BERT baseline work, ModernBERT fine-tuning/evaluation and inference packaging. Cell outputs are cleared in the committed copy to avoid publishing resume excerpts.
- `docs/model-development.md` — dataset preparation and the recorded comparison of BERT-base and ModernBERT-base.

The raw and prepared resume datasets, per-resume predictions and training artifacts are not included in this public repository.

## Deployment and monitoring

- `deploy/local/docker-compose.local.yml` — local Streamlit container configuration when FastAPI is running on the host.
- `deploy/local/docker-compose.monitoring.yml` — optional local Prometheus/Grafana services bound to loopback.
- `deploy/ec2/README.md` — record of the completed EC2 deployment and runtime components.
- `monitoring/prometheus/aws/prometheus.yml` — scrape configuration for `api:8000` on the shared Docker network.
- `monitoring/prometheus/local/prometheus.yml` — scrape configuration for an API running on the host with Prometheus in Docker Desktop.
- `monitoring/grafana/README.md` — Grafana dashboard and persistence information. The live dashboards were created in Grafana; their exported JSON is not currently tracked here.
- `docs/architecture.md` — application/network overview.

## Repository exclusions

The repository excludes the full training dataset, individual resumes, personal test files, per-resume prediction outputs, OCR logs, generated runtime metrics, Docker image layers, credentials, private keys, real environment files and Python cache artifacts. The large trained model weights are not checked into Git; the currently deployed Docker Hub API image is the verified runnable artifact containing them.
