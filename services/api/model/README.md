# ModernBERT model artifact

The FastAPI service loads a fine-tuned `answerdotai/ModernBERT-base` checkpoint from the local `model/` directory. The runtime expects these files:

- `config.json`
- `label_mapping.json`
- `model.safetensors` (approximately 570.84 MiB)
- `tokenizer.json`
- `tokenizer_config.json`

The public Git repository contains the model manifest and this inventory, but not the large trained weights file. The current Docker Hub API image was built from the complete model bundle and is the verified runtime artifact used by the AWS deployment.

Because the API Dockerfile copies the local `model/` directory, the source checkout alone does not contain every file needed to reproduce that image. The missing weights are not replaced by placeholders.
