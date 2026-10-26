# Model development notes

This document summarizes the training workflow recorded in `notebooks/ResumeClassification_Model_Development.ipynb`. The notebook contains the actual preparation and training code; this page records the decisions and aggregate results without publishing resume examples.

## Dataset preparation

The notebook loads the training split of `ahmedheakl/resume-atlas` from Hugging Face. The downloaded source snapshot contained 13,389 records across 43 categories.

Preparation included:

1. Saving a raw copy before changing the text.
2. Checking empty/short records and category counts.
3. Grouping repeated resume text and checking groups assigned to different categories.
4. Reviewing high-similarity records with conflicting labels using character TF-IDF similarity and token overlap.
5. Quarantining unresolved label-conflict groups and removing repeat records.
6. Creating the prepared `Text_prepared` representation and grouped train/validation/test splits.
7. Verifying that split labels, label mapping and duplicate-group constraints agree.
8. Auditing token lengths for BERT, DistilBERT and ModernBERT.

The final prepared dataset contained 11,864 records. The saved splits were:

| Split | Records | Share |
|---|---:|---:|
| Train | 9,473 | 79.85% |
| Validation | 1,203 | 10.14% |
| Test | 1,188 | 10.01% |
| Total | 11,864 | 100% |

The working dataset and split files are not included in this repository because they contain resume text and are large data artifacts. The notebook expects them in the Kaggle workspace path `/kaggle/working/resume_classification`.

## Model selection

The project first established a fine-tuned BERT-base baseline, then evaluated a fine-tuned ModernBERT-base checkpoint. The training code uses validation metrics to choose checkpoints; the test split is used for final reporting only.

| Metric | BERT-base | ModernBERT-base | Difference |
|---|---:|---:|---:|
| Accuracy | 88.30% | 92.09% | +3.79 percentage points |
| Balanced accuracy | 88.16% | 92.60% | +4.44 percentage points |
| Macro precision | 87.99% | 92.20% | +4.21 percentage points |
| Macro recall | 88.16% | 92.60% | +4.44 percentage points |
| Macro F1 | 87.48% | 92.12% | +4.63 percentage points |
| Weighted F1 | 88.08% | 92.06% | +3.98 percentage points |

Both runs used the same 1,188 held-out test records and 43 categories. The configured input limits differ: BERT used 512 tokens, while ModernBERT used 2,048. This reflects the intended model-specific inference settings; it is not a comparison where both models see the same maximum context length.

The selected ModernBERT checkpoint's manifest records a test loss of 0.3881. The manifest is stored in `services/api/model_manifest.json`.

## Deployed inference configuration

- Base architecture: `answerdotai/ModernBERT-base`
- Labels: 43
- Maximum input length: 2,048 tokens
- Serving: FastAPI with CPU inference in the current EC2 image
- Input: `Text_prepared`-style text for the text route, or supported resume uploads through the file route

## Reproducing the training work

The notebook is Kaggle-oriented and records the saved-workspace workflow, including recovery checks and multiple tuning iterations. It is not a clean, one-click run in a blank environment. Restore the dataset, prepared splits, tokenizers and required checkpoint paths before running the applicable sections. Model tuning requires a GPU and substantial runtime.

The public notebook has no saved cell outputs because the original data-quality outputs included snippets from resume text. Aggregate figures above are from the recorded metrics and manifest; no resume content is reproduced in this document.
