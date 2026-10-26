# FastAPI inference service

This service loads the locally packaged fine-tuned ModernBERT model at startup and serves resume classification over HTTP. It is intended to run as the private `api` container on the Docker network `resume-net`.

## Endpoints

- `GET /` — service information.
- `GET /health` — model readiness and runtime configuration.
- `GET /docs` — interactive OpenAPI documentation.
- `POST /predict` — classify text passed as `prepared_text`.
- `POST /predict-file` — extract text from supported resume files and classify.
- `GET /metrics` — Prometheus metrics. Keep this endpoint on a trusted network.

The API accepts PDF, DOCX, TXT, and supported image formats, subject to configured size/page/pixel limits. Tesseract OCR is installed by the Dockerfile for image-based text extraction. The model is loaded once during application startup.

## Local validation

From `services/api`, install runtime requirements and development test dependencies, then run `python -m pytest -q tests`. The API tests mock model inference so they do not need to load the full model. A live inference/build test still requires the complete model folder.

## Model files

The runtime expects `model/config.json`, `model/label_mapping.json`, `model/model.safetensors`, `model/tokenizer.json`, and `model/tokenizer_config.json`. The source-audit archive supplied for repository setup did not include the weights; see `model/README.md`. Do not publish a container build as release-ready until these files are provided and validated.

## Privacy

Prometheus metrics use fixed, low-cardinality labels and are designed not to include resume text, filenames, user data, or predicted category. Avoid logging request bodies or committing resume samples.
