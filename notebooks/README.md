# Model development notebook

`ResumeClassification_Model_Development.ipynb` records the Kaggle-based preparation and model development work: ResumeAtlas dataset inspection, duplicate and label-conflict review, grouped split validation, token-length analysis, BERT baseline experiments, ModernBERT training/evaluation, and packaging the selected checkpoint for inference.

The notebook references cached data and experiment artifacts under `/kaggle/working/resume_classification`. It represents the development environment and the sequence of experiments carried out there, rather than a self-contained run in a blank environment. Training uses a GPU and can take substantial time.

Cell outputs in the committed copy are cleared because some original data-quality outputs contained excerpts from resumes. Aggregate metrics are recorded in `services/api/model_manifest.json` and [the model development notes](../docs/model-development.md).

The raw training dataset, prepared resume text, per-resume prediction files and training checkpoints are not included in the public repository.
