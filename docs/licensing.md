# Source and model licensing notes

- **Application source:** this repository includes an MIT License file.
- **Training dataset:** the [ResumeAtlas dataset card](https://huggingface.co/datasets/ahmedheakl/resume-atlas) declares the MIT license.
- **Base model:** the [answerdotai/ModernBERT-base model card](https://huggingface.co/answerdotai/ModernBERT-base) declares Apache-2.0.
- **Fine-tuned checkpoint:** the checkpoint is derived from the ModernBERT base model and trained on ResumeAtlas. Review the upstream licence terms and notices before redistributing the weights or a container image; the project should not imply that the upstream licences erase privacy or data-protection obligations associated with resume data.

The public repository excludes the raw and prepared resume datasets, individual resume examples and request logs. Its training metrics are aggregate values only.
