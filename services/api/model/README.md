# ModernBERT model artifact

The FastAPI service loads a fine-tuned `answerdotai/ModernBERT-base` checkpoint from the local `model/` directory. The runtime expects these files:

- `config.json`
- `label_mapping.json`
- `model.safetensors` (approximately 570.84 MiB)
- `tokenizer.json`
- `tokenizer_config.json`

The full model artifact set is tracked in this public repository, with `model.safetensors` stored through Git LFS. The LFS pointer records a size of 598,565,908 bytes and SHA-256 `718f1481c6e7b65a043d373766d77c912aefd78648edf38663d6eb52dbeadd5a`. The local object was verified on 2026-10-27: `git lfs fsck` passed; the 598,565,908-byte size and expected SHA-256 matched; config/tokenizer loaded; and CPU inference completed with 43 finite class probabilities. Use `scripts/verify_model_artifact.py` to repeat these checks. The current Docker Hub API image remains the verified runtime artifact used by the AWS deployment.
