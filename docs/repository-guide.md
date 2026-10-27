# Repository guide

This repository contains the source, model-development record, deployment configuration and monitoring documentation for the ModernBERT ResumeClassification application.

## Application source

- `services/api/app.py` — FastAPI routes, model loading, training-consistent contact masking, document/image extraction and Prometheus metrics.
- `services/api/Dockerfile` — API runtime image definition, including Tesseract OCR and the local model directory.
- `services/api/requirements.txt` — API runtime dependencies.
- `services/api/requirements-dev.txt` — additional API regression-test dependencies.
- `services/api/tests/test_api.py` — route, validation, preprocessing and file-extraction tests with inference mocked.
- `services/api/tests/test_model_smoke.py` — opt-in test that loads the real checkpoint and runs CPU inference.
- `services/api/scripts/verify_model_artifact.py` — checks model weight size/hash, label mapping, config and tokenizer; optional full model-load inference check.
- `services/api/scripts/diagnose_image_ocr.py` — diagnostic tool for OCR extraction quality. Its output may contain extracted resume text and should remain private.
- `services/api/model_manifest.json` — model architecture, category count, input limit, evaluation metrics and artifact-verification status.
- `services/api/model/` — model configuration, label mapping, tokenizer files and the Git LFS-tracked checkpoint.

- `services/frontend/streamlit_app.py` — user interface for text input, resume upload and prediction display.
- `services/frontend/Dockerfile` and `requirements.txt` — UI image and runtime dependencies.

## Model development

- `notebooks/ResumeClassification_Model_Development.ipynb` — Kaggle notebook covering data-quality checks, duplicate/conflicting-label review, grouped splits, BERT baseline, ModernBERT tuning/evaluation and inference packaging. Outputs are cleared in the committed copy to avoid publishing resume excerpts.
- `requirements-training.txt` — separate training/data-preparation dependencies.
- `docs/model-development.md` — aggregate preparation and evaluation results.
- `docs/dataset-provenance.md` — dataset origin, recorded counts, and the fact that the historical source revision/checksum was not pinned.

Raw/prepared resume data, per-resume outputs and training artifacts remain outside this public repository.

## Deployment and monitoring

- `deploy/local/docker-compose.local.yml` — local UI container configuration when FastAPI runs on the host.
- `deploy/local/docker-compose.monitoring.yml` — optional local Prometheus/Grafana services bound to loopback.
- `deploy/ec2/docker-compose.yml` — four-service Compose definition using the published Docker Hub images and private API/Prometheus ports.
- `deploy/ec2/.env.example` — example Grafana credentials configuration; the real `.env` file is not committed.
- `deploy/ec2/README.md` — deployment record, observed verification, network/port layout and Compose migration notes.
- `monitoring/prometheus/aws/prometheus.yml` — scrape target `api:8000` on the shared Docker network.
- `monitoring/prometheus/local/prometheus.yml` — scrape target `host.docker.internal:8000` for a host-running API with Prometheus in Docker Desktop.
- `monitoring/grafana/provisioning/datasources/prometheus.yml` — default Grafana data source for a fresh Compose deployment.
- `monitoring/grafana/README.md` — description of the saved live dashboards. Their JSON has not been exported into the repository.
- `docs/architecture.md` — component and network overview.

## Excluded data

The repository excludes raw/prepared resume datasets, individual resume examples, per-resume predictions, OCR output, generated monitoring time series, Grafana runtime database files, local secrets, private keys and Python cache artifacts. The model weights are stored with Git LFS and need the actual LFS object fetched for a complete source checkout.
