# ModernBERT model artifact

The FastAPI service loads a fine-tuned `answerdotai/ModernBERT-base` checkpoint from the local `model/` directory. The runtime expects these files:

- `config.json`
- `label_mapping.json`
- `model.safetensors` (approximately 570.84 MiB)
- `tokenizer.json`
- `tokenizer_config.json`

The full model artifact set is now tracked in this public repository, with `model.safetensors` stored through Git LFS. The model-artifact commit is [7e949f5](https://github.com/atharva315/ResumeClassification-API/commit/7e949f50614a5fda8989c369f33ac88784c46ee1). Clone with Git LFS installed and fetch the LFS object before building the API image. The current Docker Hub API image remains the verified runtime artifact used by the AWS deployment.
