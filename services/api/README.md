# FastAPI inference service

The API loads a fine-tuned ModernBERT model at application startup and provides resume classification over HTTP. In the deployed application, FastAPI is the private inference service used by the Streamlit frontend and Prometheus.

## Endpoints

- `GET /` — service information.
- `GET /health` — health/model-readiness information.
- `GET /docs` — interactive OpenAPI documentation.
- `POST /predict` — classify text submitted as `prepared_text`.
- `POST /predict-file` — extract text from supported resume files and classify it.
- `GET /metrics` — Prometheus metrics.

## Preprocessing contract

The API applies Unicode normalization and removes control/format characters, then uses the same contact-detail masks as the notebook's `prepare_text()` function:

- Email-like values become `[EMAIL]`.
- URL-like values become `[URL]`.
- Recognizable phone-like digit strings become `[PHONE]`.
- Whitespace is collapsed to single spaces, matching the training representation.

These patterns are approximate and do not attempt to identify every personal identifier. The endpoint does not store submitted resume content in a database.

## Tests

`tests/test_api.py` contains route, validation, preprocessing and extraction regression tests. Model inference is mocked there, so the tests do not need to load the large checkpoint.

`tests/test_model_smoke.py` is a separate opt-in test that loads the genuine local checkpoint and runs CPU inference. Set `RUN_REAL_MODEL_SMOKE=1` when running it. `scripts/verify_model_artifact.py` checks the expected LFS weight size and SHA-256, model config, label mapping and tokenizer; its `--load-model` option additionally loads the checkpoint and runs a real inference.

## Model artifact

The runtime expects `model/config.json`, `model/label_mapping.json`, `model/model.safetensors`, `model/tokenizer.json`, and `model/tokenizer_config.json`. The 598,565,908-byte trained weights file is stored through Git LFS. Its expected SHA-256 is recorded in `model_manifest.json`. The GitHub push reported the LFS upload complete, but the local checksum and model-load validation are still pending.

## Runtime and image size

The currently deployed Docker Hub image is the tested production artifact and has not been replaced by these source changes. The API requirements currently leave PyTorch's version/build selection broad, which can make clean image builds less reproducible and can include more libraries than needed for CPU inference. PyTorch publishes CPU-only wheels, so a CPU-specific candidate build is technically feasible; it must be tested against this exact ModernBERT checkpoint and all endpoints before it is used to replace the existing image.
