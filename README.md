# ResumeClassification — ModernBERT Resume Classifier

An end-to-end resume classification application built with **ModernBERT, FastAPI, Streamlit, Docker, AWS EC2, Prometheus, and Grafana**. It classifies resume text and supported resume files into 43 professional categories.

> **Deployment note:** The public demo runs on an AWS EC2 instance that may be stopped to control costs. When the instance is stopped, the website and monitoring dashboards are offline. The instance's public IPv4 address may change after restart.

## Features

- Fine-tuned ModernBERT classifier with 43 job categories.
- Streamlit interface for pasting resume text or uploading PDF, DOCX, TXT, PNG, or JPEG files.
- FastAPI inference service with health and readiness information, prediction endpoints, and Prometheus-compatible metrics.
- Top prediction and four alternative categories where the model's confidence policy allows a prediction.
- Docker images published to Docker Hub for the currently deployed UI and API.
- AWS EC2 deployment with Docker networking.
- Prometheus metrics collection and Grafana dashboards.
- No database or Redis; the application is designed not to persist submitted resumes as an application data store.

## Architecture

```text
Browser
  |
  | HTTP :8501
  v
Streamlit UI container (ui)
  |
  | Docker network: resume-net
  | http://api:8000
  v
FastAPI container (api) ---- /metrics ----> Prometheus container
                                               |
                                               v
                                         Grafana container
                                         browser port :3000
```

Prometheus and the API communicate on the Docker network. The API's port 8000 should not be published to the public internet. Prometheus port 9090 should remain private. Grafana's port 3000 should be restricted by the EC2 security group to an administrator's current IP.

## Technology stack

| Area | Technology |
|---|---|
| Model | Fine-tuned answerdotai/ModernBERT-base |
| Model task | Multi-class text classification, 43 categories |
| API | FastAPI, Uvicorn, Python |
| UI | Streamlit, Requests |
| File extraction | PyMuPDF, pdfplumber, python-docx, Pillow, Tesseract OCR |
| Containers | Docker |
| Image registry | Docker Hub |
| Cloud | AWS EC2, region `ap-southeast-2` (Sydney) |
| Metrics | prometheus-client and Prometheus |
| Dashboards | Grafana OSS |

## Dataset preparation

The documented data preparation pipeline started with **13,389 records** and produced **11,864 prepared records** across 43 job categories. The recorded split was:

| Split | Records |
|---|---:|
| Train | 9,473 |
| Validation | 1,203 |
| Test | 1,188 |
| **Total prepared** | **11,864** |

Preparation included text cleaning, duplicate handling and train/validation/test splitting. BERT, DistilBERT and ModernBERT fine-tuning approaches were explored; the deployed inference service uses the selected ModernBERT model. Dataset files, raw resumes and training artifacts are not included in this public repository.

## Model evaluation

The committed model manifest records these evaluation results on 1,188 held-out test samples:

| Metric | Recorded value |
|---|---:|
| Accuracy | 92.09% |
| Macro F1 | 92.12% |
| Weighted F1 | 92.06% |
| Test loss | 0.3881 |
| Test samples | 1,188 |

These figures describe the recorded evaluation, not a guarantee of production accuracy. Evaluation and runtime preprocessing must remain consistent. The configured maximum input length is 2,048 tokens.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health/model readiness check |
| GET | `/docs` | Interactive OpenAPI documentation |
| POST | `/predict` | Classify prepared resume text |
| POST | `/predict-file` | Extract supported resume files and classify |
| GET | `/metrics` | Prometheus metrics; keep on a trusted network |

For text inference, the UI sends JSON using the `prepared_text` field. The API response includes `predicted_category`, `other_categories`, a prediction message, token-limit/truncation details, inference timings, and the model name. The API may reject short, irrelevant, repetitive, or low-confidence inputs rather than returning a category.

Example text request (the sample includes sufficient resume-related content for the input suitability check):

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"prepared_text":"Professional summary: Python developer experienced in building backend applications and REST APIs. Skills include Python, FastAPI, SQL, Docker, AWS, automated testing, debugging and Git. Education: bachelor degree in computer engineering. Experience: developed services, deployed applications, collaborated with product teams, maintained production systems and improved application reliability."}'
```

Example file request:

```bash
curl -X POST "http://localhost:8000/predict-file" \
  -F "file=@./resume.pdf"
```

Use your own synthetic or authorized test resume file; do not commit personal resume files to the repository.

## Docker Hub images

The currently deployed images are:

- API: `rockstar1505/resume-classification-api:latest`
- UI: `rockstar1505/resumeclassification-ui:latest`

The running AWS deployment was created with Docker containers on the `resume-net` network. Docker Hub stores the built images; this Git repository stores source and configuration, not a copy of the multi-gigabyte container images.

## AWS EC2 deployment

The current environment is an EC2 instance in Sydney (`ap-southeast-2`). The four existing container names are:

- `api` — FastAPI, internal port 8000
- `ui` — Streamlit, published port 8501
- `prometheus` — metrics scraper, internal port 9090
- `grafana` — dashboards, published port 3000 and restricted by the security group

The containers were configured with `--restart unless-stopped` and Prometheus/Grafana have persistent Docker volumes. Do not run `docker compose down -v`, remove named volumes, or recreate the monitoring containers as part of an application update.

For the cost-conscious demo workflow, start EC2 before testing or deploying and stop it afterward. The app and monitoring will be unavailable while stopped. EBS storage and other associated resources may still incur charges.

See [deployment notes](deploy/ec2/README.md) for the current runtime model and safe-update expectations.

## Repository layout

```text
services/
  api/          FastAPI source, dependency list, Dockerfile, tests
  frontend/     Streamlit UI and its Docker build
deploy/
  local/        Local UI development instructions/configuration
  ec2/          AWS runtime and safe deployment documentation
monitoring/
  prometheus/   Local and Docker-network scrape configurations
  grafana/      Dashboard/provisioning notes
docs/           Architecture and CI/CD roadmap
.github/
  workflows/    Reserved for future validation and release workflows
```

## Model artifact availability

The API requires the complete local `model/` directory: `config.json`, `label_mapping.json`, `model.safetensors`, `tokenizer.json`, and `tokenizer_config.json`. The trained weights are approximately 570.84 MB and are **not currently stored in this source repository**.

The existing Docker Hub API image contains the trained model and remains the known deployment artifact for the current service. A clean API image build from this repository is not yet reproducible; before enabling API CI/CD, add the genuine checkpoint through Git LFS or an approved artifact source and validate the clean build and model startup. No placeholder weights are used.

## Privacy and security

- Never commit credentials, API tokens, private keys, real `.env` files, real resumes, or OCR output containing personal information.
- Keep API port 8000 and Prometheus port 9090 private.
- Restrict Grafana port 3000 to a trusted IP; do not expose it to `0.0.0.0/0`.
- Avoid logging submitted resume content.
- Classification is decision support; a person should review results before hiring decisions.

## CI/CD roadmap

The next phase will add GitHub Actions for validation and building/publishing versioned Docker images to Docker Hub, followed by a controlled deployment to the existing EC2 instance. API image builds must remain blocked until model artifact handling is solved. The deployment workflow must update only `api` and `ui`, preserve the monitoring volumes, verify health, and avoid automatically starting EC2 on every push.

See [architecture notes](docs/architecture.md) and [CI/CD plan](docs/cicd-roadmap.md).

## License

See [LICENSE](LICENSE).