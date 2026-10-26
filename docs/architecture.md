# Architecture and operational design

## Request path

1. The browser connects to Streamlit on port 8501.
2. Streamlit sends pasted text to `POST /predict` with `prepared_text`, or uploads a file to `POST /predict-file`.
3. FastAPI extracts/prepares input, checks suitability and score rules, loads the local ModernBERT model once at startup, and returns a primary category with up to four alternatives.
4. FastAPI exposes `/health` for readiness and `/metrics` for Prometheus.
5. Prometheus scrapes the API using Docker DNS (`api:8000`); Grafana queries Prometheus and renders dashboards.

## Observability metrics

The API emits low-cardinality HTTP request counters and latency histograms, prediction-result counts, stage-duration histograms, and model-ready status. The metrics middleware excludes `/metrics` scrape traffic from application request counters. It is designed not to label metrics with resume text, filenames, user data, or predicted categories.

## Runtime safety

All four containers run on the existing `resume-net` network. API and Prometheus ports are internal to Docker. Only the UI and restricted Grafana access are published on the EC2 host. Prometheus/Grafana use named volumes. Never run `docker compose down -v` or delete these volumes as part of an application deployment.

## Model and evaluation

The model manifest records an evaluation on 1,188 test samples: accuracy 92.09%, macro F1 92.12%, and weighted F1 92.06%. Treat these as recorded offline evaluation metrics, not guaranteed live performance. The actual model files are large and were excluded from the source-audit archive; a clean source build is pending adding the genuine checkpoint.
