import numpy as np
from scipy.linalg import eigvals
from rshl_kernel import WoodburyEngine

def test_woodbury_inverse_identity():
    """
    Verifies: (I + εSS^T)^-1 == I - εS(I + εS^TS)⁻¹S^T
    """
    n, k, eps = 64, 4, 0.01
    S = np.random.randn(n, k) * 0.1

    # Ground truth (O(n^3))
    G = np.eye(n) + eps * S @ S.T
    G_inv_truth = np.linalg.inv(G)

    # Woodbury approximation (O(k^3 + nk^2))
    inner = np.eye(k) + eps * S.T @ S
    inv_inner = np.linalg.inv(inner)
    G_inv_woodbury = np.eye(n) - eps * S @ inv_inner @ S.T

    # Assert numerical equivalence
    assert np.allclose(G_inv_truth, G_inv_woodbury, atol=1e-8), "Woodbury identity failed"

def test_sylvester_determinant_identity():
    """
    Verifies: det(I_n + εSS^T) == det(I_k + εS^TS)
    """
    n, k, eps = 64, 4, 0.01
    S = np.random.randn(n, k) * 0.1

    det_n = np.linalg.det(np.eye(n) + eps * S @ S.T)
    det_k = np.linalg.det(np.eye(k) + eps * S.T @ S)

    assert np.isclose(det_n, det_k, atol=1e-8), "Sylvester determinant identity failed"

def test_engine_execution():
    """
    Verifies that the full WoodburyEngine pipeline executes without error.

    The engine records milestones every 100 iterations, so the smoke test
    must execute at least 100 iterations to verify that output path.
    """
    engine = WoodburyEngine(n=32, k=2, eps=0.01, max_it=100, dt=0.001, seed=42)
    result = engine.run()

    assert result["exec_time"] > 0
    assert len(result["milestones"]) > 0
    assert result["milestones"][-1]["rho"] > 0
