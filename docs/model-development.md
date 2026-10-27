# Model development notes

This document summarizes the training workflow recorded in `notebooks/ResumeClassification_Model_Development.ipynb`. The notebook contains the preparation and training code; this page records technical decisions and aggregate results without reproducing resume examples.

## Dataset preparation

The notebook loads the training split of `ahmedheakl/resume-atlas` from Hugging Face. The saved source snapshot contained 13,389 records across 43 categories.

Preparation included checking missing/short records and category counts; grouping repeated text; reviewing exact duplicates with conflicting labels; examining near-duplicate candidates; quarantining unresolved conflicts; preparing the `Text_prepared` representation; creating leakage-aware grouped train/validation/test splits; and auditing token lengths for BERT, DistilBERT and ModernBERT.

The prepared dataset contained 11,864 records:

| Split | Records | Share |
|---|---:|---:|
| Train | 9,473 | 79.85% |
| Validation | 1,203 | 10.14% |
| Test | 1,188 | 10.01% |
| Total | 11,864 | 100% |

The prepared data and split files remain in the private training workspace because they contain resume text and are large data artifacts. Their working path is `/kaggle/working/resume_classification`.

The notebook did not pin a Hugging Face dataset revision or record a raw-snapshot checksum at acquisition time. The historical revision and checksum therefore cannot be recovered from this notebook alone; see [dataset provenance](dataset-provenance.md).

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

Both models used the same 1,188 held-out test records and 43 categories. BERT used a configured 512-token input limit; ModernBERT used 2,048 tokens. This compares the selected model configurations rather than both models at the same context length.

## Serving contract

Training's `prepare_text()` function replaces recognizable contact details with `[EMAIL]`, `[URL]` and `[PHONE]` markers, then collapses whitespace to a single space. The API's `normalize_resume_text()` now applies the same contact masks and whitespace convention, after its Unicode and control-character normalization. Regression tests cover standard and flattened contact formats.

## Notebook context

The notebook uses saved Kaggle workspace files, including prepared splits, tokenizer artifacts, model checkpoints, training histories and reports. It is a record of the actual experiment sequence, not a one-click training job in an empty environment. Training requires a compatible GPU and can take substantial time.

Cell outputs are cleared from the public copy because original data-quality output contained resume excerpts. The raw dataset, prepared resume text, per-resume outputs and training checkpoints remain outside the public repository.
