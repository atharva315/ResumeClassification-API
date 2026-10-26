# FastAPI inference service

The API loads a fine-tuned ModernBERT model at application startup and provides resume classification over HTTP. In the deployed application, FastAPI is the private inference service used by the Streamlit frontend and Prometheus.

## Endpoints

- `GET /` — service information.
- `GET /health` — health/model-readiness information.
- `GET /docs` — interactive OpenAPI documentation.
- `POST /predict` — classify text submitted as `prepared_text`.
- `POST /predict-file` — extract text from supported resume files and classify it.
- `GET /metrics` — Prometheus metrics.

Supported file formats include PDF, DOCX, TXT and supported image formats, subject to request and extraction limits. Tesseract OCR is included in the container for image text extraction. The model is loaded once at startup; predictions use the prepared-text representation established during training.

## Tests

`tests/test_api.py` contains route, validation and extraction regression tests with model loading/inference mocked. The tests do not require the full model weights.

## Model artifacts

The runtime expects `model/config.json`, `model/label_mapping.json`, `model/model.safetensors`, `model/tokenizer.json`, and `model/tokenizer_config.json`. The trained weights are approximately 570.84 MiB and are not stored in this public Git repository. The verified Docker Hub API image contains the complete model used by the current AWS service.

## Privacy

The application is designed not to persist submitted resumes in a database. Prometheus metrics use fixed, low-cardinality labels rather than resume text or filenames.
