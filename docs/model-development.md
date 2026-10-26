# Model development notes

This document summarizes the training workflow recorded in `notebooks/ResumeClassification_Model_Development.ipynb`. The notebook contains the preparation and training code; this page records the technical decisions and aggregate results without reproducing resume examples.

## Dataset preparation

The notebook loads the training split of `ahmedheakl/resume-atlas` from Hugging Face. The source snapshot contained 13,389 records across 43 categories.

Preparation included checking empty and short records, inspecting category counts, grouping repeated resume text, identifying exact duplicate text with conflicting labels, reviewing high-similarity conflict groups, removing unresolved conflicts/repeats from the prepared data, creating a `Text_prepared` representation and grouped train/validation/test splits, and auditing token lengths for BERT, DistilBERT and ModernBERT.

The final prepared dataset contained 11,864 records:

| Split | Records | Share |
|---|---:|---:|
| Train | 9,473 | 79.85% |
| Validation | 1,203 | 10.14% |
| Test | 1,188 | 10.01% |
| Total | 11,864 | 100% |

The prepared data and split files remain in the private training workspace because they contain resume text and are large data artifacts. The notebook records paths under `/kaggle/working/resume_classification`.

## Model comparison

The project established a fine-tuned BERT-base baseline, then evaluated a fine-tuned ModernBERT-base checkpoint. Model selection used validation metrics; the held-out test split was used for final reporting.

| Metric | BERT-base | ModernBERT-base | Difference |
|---|---:|---:|---:|
| Accuracy | 88.30% | 92.09% | +3.79 percentage points |
| Balanced accuracy | 88.16% | 92.60% | +4.44 percentage points |
| Macro precision | 87.99% | 92.20% | +4.21 percentage points |
| Macro recall | 88.16% | 92.60% | +4.44 percentage points |
| Macro F1 | 87.48% | 92.12% | +4.63 percentage points |
| Weighted precision | 88.77% | 92.48% | +3.71 percentage points |
| Weighted recall | 88.30% | 92.09% | +3.79 percentage points |
| Weighted F1 | 88.08% | 92.06% | +3.98 percentage points |
| Test loss | 0.5788 | 0.3881 | -0.1906 |

Both runs used the same 1,188 held-out test records and 43 categories. BERT used a configured 512-token input limit; ModernBERT used 2,048 tokens. This compares the selected model configurations, not both models at the same context length.

The selected ModernBERT checkpoint's test metrics are also recorded in `services/api/model_manifest.json`.

## Deployed inference configuration

- Base architecture: `answerdotai/ModernBERT-base`
- Output categories: 43
- Input limit: 2,048 tokens
- Serving: FastAPI with CPU inference in the current EC2 image
- Input representation: prepared text aligned with the training dataset's `Text_prepared` field

## Notebook context

The notebook follows the saved Kaggle workspace used for data preparation, recovery checks and model tuning. It references persisted splits, tokenizer files, training histories and checkpoint directories. Cell outputs have been cleared from the public copy because the original data-quality outputs included resume excerpts. The notebook source remains available; the data and checkpoints are not part of this repository.
