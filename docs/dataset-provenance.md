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

## Current upstream source-file reference

The Hugging Face file page currently reports the following for `train.csv` (checked 2026-10-27):

- File version shown on the page: commit `3fa56be`.
- Remote file size: 53.6 MB.
- SHA-256: `c71b0d6d88e75412aefb3998d289e4af8d9c07a9b26e8a974d6a2bac485480c2`.
- [Source file and file history](https://huggingface.co/datasets/ahmedheakl/resume-atlas/blob/main/train.csv).

This is a useful checksum for the currently published source file. It is **not a guaranteed historical revision identifier for the training run**, because the notebook called `load_dataset("ahmedheakl/resume-atlas", split="train")` without pinning a Hugging Face revision. The saved raw Parquet file and its checksum were not committed, so we cannot prove that the exact bytes consumed during the original run match the current source file.

The training workspace path was `/kaggle/working/resume_classification/data/raw/resume_atlas_raw.parquet`. The raw and prepared files contain resume text and remain excluded from this public repository.

For another training run, pin a specific Hugging Face commit when downloading the dataset and record the downloaded file's SHA-256 at acquisition time. Do not upload the resume dataset or any per-resume data to this repository.
