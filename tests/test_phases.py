"""Smoke and invariant tests for all nine public engines."""

import numpy as np

from rshl_kernel import (
    AdaptiveWoodburyEngine,
    HolographicProjectionEngine,
    IdentityConvergenceEngine,
    QuantumTopologicalEngine,
    RetrocausalHolographicEngine,
    RicciFlowWoodburyEngine,
    SingularityEngine,
    TopologicalRicciFlowEngine,
    WoodburyEngine,
)


def test_rank1_closed_form_inverse():
    engine = SingularityEngine(dim=8, epsilon=0.02, max_iterations=1, seed=7)
    residual = np.linalg.norm(engine.metric() @ engine.metric_inverse_closed_form() - np.eye(8))
    assert residual < 1e-10


def test_rank1_logdet_identity():
    engine = SingularityEngine(dim=8, epsilon=0.02, max_iterations=1, seed=7)
    assert np.isclose(np.linalg.slogdet(engine.metric())[1], engine.logdet_metric_closed_form(), atol=1e-12)


def test_woodbury_inverse_identity_against_dense_reference():
    engine = WoodburyEngine(n=16, k=3, eps=0.02, max_it=1, seed=7)
    G = np.eye(engine.n) + engine.eps * engine.S @ engine.S.T
    residual = np.linalg.norm(G @ engine.woodbury_inverse() - np.eye(engine.n))
    assert residual < 1e-10


def test_adaptive_epsilon_is_positive():
    engine = AdaptiveWoodburyEngine(n=16, k=3, seed=7)
    assert engine.get_adaptive_eps() > 0


def test_ricci_epsilon_floor():
    engine = RicciFlowWoodburyEngine(n=16, k=3, eps0=0.01, seed=7)
    for _ in range(5):
        engine.ricci_adaptation_step()
    assert engine.eps >= 1e-6


def test_topology_output_shape():
    engine = TopologicalRicciFlowEngine(n=16, k=3, max_it=1, seed=7)
    betti = engine.compute_persistent_homology_approx()
    assert len(betti) == 5
    assert all(len(item) == 3 for item in betti)


def test_quantum_state_remains_normalized():
    engine = QuantumTopologicalEngine(n=12, k=3, max_it=1, seed=7)
    adjacency, degrees = engine.get_graph_properties()
    H = engine.build_hamiltonian(adjacency, degrees, engine.compute_curvature_proxy())
    engine.evolve_quantum_state(H)
    assert np.isclose(np.linalg.norm(engine.psi), 1.0, atol=1e-10)


def test_holographic_projection_dimensions():
    engine = HolographicProjectionEngine(bulk_dim=4, boundary_size=8, seed=7)
    _, history = engine.execute(steps=1)
    assert engine.boundary_reality.shape == (8, 8)
    assert len(history) == 1


def test_retrocausal_density_matrix_is_valid():
    engine = RetrocausalHolographicEngine(bulk_dim=4, boundary_size=8, seed=7)
    engine.retrocausal_optimization_step(learning_rate=0.1)
    rho = engine.bulk_rho
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    assert np.isclose(np.trace(rho), 1.0, atol=1e-10)
    assert np.min(np.linalg.eigvalsh(rho)) >= -1e-10


def test_identity_convergence_alignment_is_bounded():
    result = IdentityConvergenceEngine(steps=5).run()
    assert -1.0 <= result["final_alignment"] <= 1.0
    assert result["final_relative_entropy"] >= 0.0
