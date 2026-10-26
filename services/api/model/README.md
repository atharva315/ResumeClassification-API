# Trained model artifact required at runtime

The API Dockerfile copies this directory into the image, and FastAPI loads the model from this local path with `local_files_only=True`. The full model must be present before building a runnable API image.

Required files (confirmed from the local model inventory):

- `config.json`
- `label_mapping.json`
- `model.safetensors` (approximately 570.84 MiB)
- `tokenizer.json` (approximately 3.42 MiB)
- `tokenizer_config.json`

The genuine model files are not currently committed here. Do not create placeholder weights. Add the trained checkpoint through Git LFS or an approved artifact store, then validate a clean Docker build and API startup before enabling API image CI/CD. The root `.gitattributes` is configured for `.safetensors` tracking with Git LFS.
