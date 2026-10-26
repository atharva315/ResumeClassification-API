# Notebooks

`ResumeClassification_Model_Development.ipynb` is the project development notebook used for dataset validation, duplicate/conflict review, prepared split verification, BERT baseline training/evaluation, ModernBERT tuning, final evaluation and packaging the inference bundle.

It is a record of the actual work carried out in Kaggle, not a single-click training pipeline. It relies on project artifacts under `/kaggle/working/resume_classification`, including the prepared split files and tokenizers. Training cells require a GPU and can run for a long time.

The committed copy has execution outputs cleared because some original outputs contained excerpts from resumes during data-quality review. The code cells remain; aggregate results are documented in [model development notes](../docs/model-development.md) and `services/api/model_manifest.json`.

Do not upload raw resumes, prepared resume datasets, prediction-by-resume CSVs, or outputs containing personal information to this repository.
