"""Verify the checked-out model artifact and optionally run real CPU inference.

Run from services/api:
    python scripts/verify_model_artifact.py
    python scripts/verify_model_artifact.py --load-model
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

EXPECTED_WEIGHT_SIZE = 598_565_908
EXPECTED_WEIGHT_SHA256 = "718f1481c6e7b65a043d373766d77c912aefd78648edf38663d6eb52dbeadd5a"
EXPECTED_LABELS = 43
API_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = API_DIR / "model"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--load-model",
        action="store_true",
        help="Load the real tokenizer and model on CPU and run a one-text inference smoke test.",
    )
    args = parser.parse_args()

    required_files = [
        "config.json",
        "label_mapping.json",
        "model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json",
    ]
    missing = [name for name in required_files if not (MODEL_DIR / name).is_file()]
    if missing:
        print(f"FAIL: missing model files: {', '.join(missing)}", file=sys.stderr)
        print("Install Git LFS and fetch the model object before retrying.", file=sys.stderr)
        return 1

    weights = MODEL_DIR / "model.safetensors"
    size = weights.stat().st_size
    if size != EXPECTED_WEIGHT_SIZE:
        with weights.open("rb") as stream:
            prefix = stream.read(160)
        if prefix.startswith(b"version https://git-lfs.github.com/spec/v1"):
            print("FAIL: model.safetensors is only a Git LFS pointer, not the model weights.", file=sys.stderr)
        else:
            print(f"FAIL: expected {EXPECTED_WEIGHT_SIZE} bytes, found {size}.", file=sys.stderr)
        return 1

    actual_hash = sha256_file(weights)
    if actual_hash != EXPECTED_WEIGHT_SHA256:
        print(f"FAIL: SHA-256 mismatch: {actual_hash}", file=sys.stderr)
        return 1

    with (MODEL_DIR / "label_mapping.json").open(encoding="utf-8") as stream:
        mapping = json.load(stream)
    label2id = mapping.get("label2id")
    if not isinstance(label2id, dict) or len(label2id) != EXPECTED_LABELS:
        print("FAIL: label_mapping.json does not contain 43 labels.", file=sys.stderr)
        return 1
    if sorted(int(value) for value in label2id.values()) != list(range(EXPECTED_LABELS)):
        print("FAIL: label IDs must be consecutive integers from 0 to 42.", file=sys.stderr)
        return 1

    print(f"PASS: model.safetensors size = {size:,} bytes")
    print(f"PASS: model.safetensors SHA-256 = {actual_hash}")
    print(f"PASS: label mapping contains {len(label2id)} consecutive classes")

    try:
        from transformers import AutoConfig, AutoTokenizer
        config = AutoConfig.from_pretrained(str(MODEL_DIR), local_files_only=True)
        tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True)
    except Exception as exc:
        print(f"FAIL: model config/tokenizer could not load: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if int(config.num_labels) != EXPECTED_LABELS:
        print(f"FAIL: model config has {config.num_labels} labels, expected {EXPECTED_LABELS}.", file=sys.stderr)
        return 1
    print("PASS: model config and tokenizer load locally")

    if not args.load_model:
        print("Artifact verification passed. Run with --load-model for a real inference smoke test.")
        return 0

    try:
        import torch
        from transformers import AutoModelForSequenceClassification

        model = AutoModelForSequenceClassification.from_pretrained(
            str(MODEL_DIR), local_files_only=True
        ).to("cpu")
        model.eval()
        sample = (
            "Professional Summary Python developer with experience building backend services. "
            "Skills include Python, FastAPI, REST APIs, SQL, testing, debugging, deployment, "
            "Git, software maintenance and collaboration. Education includes an engineering "
            "degree. Project work includes implementing APIs and maintaining production services."
        )
        encoded = tokenizer(sample, return_tensors="pt", truncation=True, max_length=2048)
        with torch.inference_mode():
            logits = model(**encoded).logits
            probabilities = torch.softmax(logits.float(), dim=-1)
        if tuple(logits.shape) != (1, EXPECTED_LABELS):
            raise RuntimeError(f"Unexpected logits shape: {tuple(logits.shape)}")
        if not bool(torch.isfinite(probabilities).all()):
            raise RuntimeError("Inference produced non-finite probabilities.")
        if not torch.isclose(probabilities.sum(), torch.tensor(1.0), atol=1e-4):
            raise RuntimeError("Output probabilities do not sum to approximately 1.")
        print("PASS: real CPU inference completed with 43 finite class probabilities")
    except Exception as exc:
        print(f"FAIL: real model inference failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
