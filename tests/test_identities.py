"""Numerical verification of the core matrix identities and engine smoke path."""

import numpy as np

from rshl_kernel import WoodburyEngine


def test_woodbury_inverse_identity():
    """Verify the exact Woodbury inverse against a dense reference."""
    n, k, eps = 64, 4, 0.01
    rng = np.random.default_rng(42)
    S = rng.standard_normal((n, k)) * 0.1

    G = np.eye(n) + eps * S @ S.T
    G_inv_truth = np.linalg.inv(G)
    inner = np.eye(k) + eps * S.T @ S
    G_inv_woodbury = np.eye(n) - eps * S @ np.linalg.solve(inner, S.T)

    assert np.allclose(G_inv_truth, G_inv_woodbury, atol=1e-8), "Woodbury identity failed"


def test_sylvester_determinant_identity():
    """Verify det(I_n + eps*S*S^T) == det(I_k + eps*S^T*S)."""
    n, k, eps = 64, 4, 0.01
    rng = np.random.default_rng(42)
    S = rng.standard_normal((n, k)) * 0.1

    sign_n, logdet_n = np.linalg.slogdet(np.eye(n) + eps * S @ S.T)
    sign_k, logdet_k = np.linalg.slogdet(np.eye(k) + eps * S.T @ S)

    assert sign_n == sign_k == 1
    assert np.isclose(logdet_n, logdet_k, atol=1e-10), "Sylvester identity failed"


def test_engine_execution():
    """Verify the WoodburyEngine pipeline reaches and records a milestone."""
    engine = WoodburyEngine(n=32, k=2, eps=0.01, max_it=100, dt=0.001, seed=42)
    result = engine.run()

    assert result["exec_time"] > 0
    assert len(result["milestones"]) > 0
    assert result["milestones"][-1]["rho"] > 0
