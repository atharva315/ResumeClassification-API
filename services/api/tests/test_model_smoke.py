"""Opt-in smoke test that loads the genuine ModernBERT checkpoint and runs inference.

Run from services/api after fetching Git LFS objects:
    $env:RUN_REAL_MODEL_SMOKE = "1"
    python -m pytest -q tests/test_model_smoke.py
"""
import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_REAL_MODEL_SMOKE") != "1",
    reason="Set RUN_REAL_MODEL_SMOKE=1 to run the large real-model smoke test.",
)


def test_real_model_loads_and_runs_cpu_inference():
    import torch
    from fastapi.testclient import TestClient

    import app as api

    sample = (
        "Professional Summary Python developer with experience building backend services. "
        "Skills include Python, FastAPI, REST APIs, SQL, testing, debugging, deployment, "
        "Git, software maintenance and collaboration. Education includes an engineering "
        "degree. Project work includes implementing APIs and maintaining production services."
    )

    # TestClient enters the application's real lifespan; this loads the local
    # checkpoint without mocking the tokenizer or model.
    with TestClient(api.app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"
        assert health.json()["classes"] == 43

        probabilities = api.get_probabilities(sample)
        assert tuple(probabilities.shape) == (43,)
        assert bool(torch.isfinite(probabilities).all())
        assert torch.isclose(
            probabilities.sum(), torch.tensor(1.0), atol=1e-4
        )
