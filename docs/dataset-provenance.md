# Dataset provenance

| Field | Recorded value |
|---|---|
| Dataset | [ResumeAtlas](https://huggingface.co/datasets/ahmedheakl/resume-atlas) |
| Dataset identifier | `ahmedheakl/resume-atlas` |
| Split used | `train` |
| Raw records in the saved source snapshot | 13,389 |
| Categories | 43 |
| Prepared records after quality checks | 11,864 |
| Train / validation / test | 9,473 / 1,203 / 1,188 |

## Revision and checksum

The training notebook loads the dataset by repository identifier and split, without a pinned Hugging Face commit revision. The original raw Parquet file and its checksum were not saved in the public repository, so the exact historical revision and snapshot checksum cannot be reconstructed from the notebook alone. The current Hugging Face repository HEAD must not be retroactively described as the training revision.

The training workspace path was `/kaggle/working/resume_classification/data/raw/resume_atlas_raw.parquet`. The raw and prepared files contain resume text and remain excluded from this public repository.

For a future repeatable dataset download, record the resolved Hugging Face commit hash and SHA-256 of the downloaded raw artifact at acquisition time. Do not upload the resume dataset or a checksum report that includes individual resume text.
