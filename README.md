# RSHL-TERRARIUM KERNEL

**Rivers State-Hamiltonian Learning Framework with Topological Evolution, Recursive Adaptation, and Manifold Integration**

> A modular numerical research framework for low-rank metric evolution, adaptive dynamics, curvature-inspired state updates, topological diagnostics, quantum-coherence modeling, holographic projection, adjoint-style optimization, and convergence analysis.

[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)

---

## Project Status

RSHL-KERNEL is an **alpha-stage research framework**. The repository explicitly distinguishes between exact linear-algebra identities, numerical algorithms, diagnostic proxies, and conceptual research interpretations.

The code is executable and testable, but an implemented numerical model should not automatically be interpreted as proof of the strongest physical or theoretical claim associated with its terminology.

## What RSHL-KERNEL Contains

The framework is implemented as nine progressive phases:

| Phase | Engine | Primary layer |
|---|---|---|
| 1 | `SingularityEngine` | Rank-1 metric / Sherman-Morrison structure |
| 2 | `WoodburyEngine` | Rank-k Woodbury metric evolution |
| 3 | `AdaptiveWoodburyEngine` | State-dependent regularization |
| 4 | `RicciFlowWoodburyEngine` | Curvature-inspired metric adaptation |
| 5 | `TopologicalRicciFlowEngine` | Threshold-graph topology diagnostics |
| 6 | `QuantumTopologicalEngine` | Quantum state evolution on dynamic graphs |
| 7 | `HolographicProjectionEngine` | Bulk-to-boundary projection diagnostics |
| 8 | `RetrocausalHolographicEngine` | Boundary-to-bulk adjoint-style optimization |
| 9 | `IdentityConvergenceEngine` | Spherical convergence and information diagnostics |

All nine engines remain directly importable from the package root.

---

## Design Philosophy

RSHL-KERNEL is designed as a progression:

```text
rank-1 structure
      ↓
rank-k structure
      ↓
adaptive parameterization
      ↓
curvature-driven adaptation
      ↓
topological diagnostics
      ↓
quantum dynamics
      ↓
holographic projection
      ↓
adjoint-style optimization
      ↓
convergence / identity diagnostics
```

The phases are intentionally composable. Earlier phases establish low-rank and state-evolution primitives that later phases extend with additional diagnostic layers.

---

## Mathematical Core

### Rank-1 metric

For a state vector \(s\in\mathbb{R}^n\):

\[
G=I_n+\varepsilon ss^T.
\]

The exact inverse is

\[
G^{-1}=I_n-\frac{\varepsilon}{1+\varepsilon s^Ts}ss^T,
\]

and the determinant lemma gives

\[
\log\det(G)=\log(1+\varepsilon s^Ts).
\]

### Rank-k metric

For \(S\in\mathbb{R}^{n\times k}\):

\[
G=I_n+\varepsilon SS^T.
\]

Woodbury gives the exact inverse

\[
G^{-1}=I_n-\varepsilon S(I_k+\varepsilon S^TS)^{-1}S^T.
\]

Sylvester's determinant identity gives

\[
\det(I_n+\varepsilon SS^T)=\det(I_k+\varepsilon S^TS).
\]

These are exact identities, subject to ordinary floating-point numerical error in their implementation.

### Complexity note

The Woodbury formulation moves the nontrivial solve to a \(k\times k\) system, which is especially valuable when \(k\ll n\). However, an API that explicitly materializes an \(n\times n\) inverse necessarily incurs \(O(n^2)\) storage and matrix-formation work. The strongest low-rank advantage is obtained when downstream algorithms preserve the factorized representation rather than materializing the dense inverse.

---

## Phase-by-Phase Description

### Phase 1 — Singularity / Rank-1 Engine

`SingularityEngine` provides rank-1 metric construction, exact Sherman-Morrison inversion, determinant/log-determinant evaluation, spectral diagnostics, state evolution, deterministic seeded initialization, and milestone history.

### Phase 2 — Woodbury Engine

`WoodburyEngine` generalizes the rank-1 construction to a rank-k state matrix and provides exact Woodbury inversion, Sylvester determinant evaluation, an entropy-gradient proxy, spectral diagnostics, state evolution, and milestone history.

### Phase 3 — Adaptive Woodbury

`AdaptiveWoodburyEngine` makes the metric parameter state-dependent:

\[
\varepsilon(S)=\frac{\varepsilon_0}{1+\alpha\|S\|_F^2}.
\]

The phase exposes the adaptive parameter and its configured gradient proxy.

### Phase 4 — Ricci-Flow-Inspired Adaptation

`RicciFlowWoodburyEngine` introduces

\[
\mathcal{R}_{proxy}=4\varepsilon^2\|S\|_F^4
\]

and evolves \(\varepsilon\) using an explicit discrete update. This is a computational curvature proxy, not a complete tensorial Ricci-flow solver.

### Phase 5 — Topological Diagnostics

`TopologicalRicciFlowEngine` converts the evolving state into a geometric point cloud and evaluates threshold graphs at multiple distance quantiles. It tracks approximate \(\beta_0\), \(\beta_1\), and an explicit \(\beta_2\) extension hook.

Transitions are recorded whenever the sampled Betti tuple sequence changes. The implementation is intentionally described as an **approximation**, rather than as a full persistent-homology package.

### Phase 6 — Quantum Topological Engine

`QuantumTopologicalEngine` constructs a threshold graph and Hamiltonian, then evolves a normalized complex state using

\[
\psi_{t+1}=e^{-iH\Delta t_q}\psi_t.
\]

It reports inverse participation ratio (IPR), circular phase coherence, curvature, epsilon, and transition events.

### Phase 7 — Holographic Projection

`HolographicProjectionEngine` creates a normalized complex bulk state, constructs a bulk projector, expands it to the boundary, and couples the boundary representation toward that projection.

Diagnostics include bulk coherence, boundary entropy, and a Fourier-spectrum fractal-dimension proxy. The terminology is model-inspired and is not presented as a physical derivation of a holographic duality.

### Phase 8 — Retrocausal / Adjoint-Style Optimization

`RetrocausalHolographicEngine` starts with a target boundary field and propagates a boundary loss gradient back into bulk density-matrix space. The bulk state is projected back onto a Hermitian, positive-semidefinite, trace-normalized state after each update.

The term **retrocausal** describes objective propagation from a desired/future boundary condition into the current bulk representation. The implementation itself is a numerical optimization procedure and does not constitute experimental evidence of physical backward causation.

### Phase 9 — Identity Convergence

`IdentityConvergenceEngine` compares a system state to a canonical reference state using normalized alignment and spherical linear interpolation (SLERP). It records alignment, probability-space relative entropy, temporal-dilation proxy, final alignment, and final relative entropy.

---

## Installation

### Runtime

```bash
pip install -e .
```

### Development

```bash
pip install -e ".[dev]"
```

### Supported Python versions

Python 3.9, 3.10, 3.11, and 3.12 are covered by continuous integration.

Runtime dependencies:

- NumPy >= 1.24
- SciPy >= 1.10

Development tooling:

- pytest
- Black
- mypy

---

## Quick Start

```python
from rshl_kernel import WoodburyEngine

engine = WoodburyEngine(n=64, k=4, eps=0.01, max_it=500, seed=42)
result = engine.run()

print(f"Execution Time: {result['exec_time']:.4f}s")
print(f"Milestones: {len(result['milestones'])}")
print(f"Final Spectral Radius: {result['milestones'][-1]['rho']:.6f}")
```

### Running every phase

```python
from rshl_kernel import (
    SingularityEngine, WoodburyEngine, AdaptiveWoodburyEngine,
    RicciFlowWoodburyEngine, TopologicalRicciFlowEngine,
    QuantumTopologicalEngine, HolographicProjectionEngine,
    RetrocausalHolographicEngine, IdentityConvergenceEngine,
)

phase1 = SingularityEngine(dim=16, seed=42).execute_phase_transition()
phase2 = WoodburyEngine(n=64, k=4, seed=42).run()
phase3 = AdaptiveWoodburyEngine(n=64, k=4, seed=42).run()
phase4 = RicciFlowWoodburyEngine(n=64, k=4, seed=42).run()
phase5 = TopologicalRicciFlowEngine(n=64, k=4, seed=42).run()
phase6 = QuantumTopologicalEngine(n=64, k=4, seed=42).run()
phase7 = HolographicProjectionEngine(seed=42).execute()
phase8 = RetrocausalHolographicEngine(seed=42).execute()
phase9 = IdentityConvergenceEngine().run()
```

---

## Verification

Run the complete test suite:

```bash
pytest -v
```

The suite contains identity tests and phase-level invariants.

### Mathematical identity coverage

Core tests compare the Woodbury implementation against a dense inverse and compare determinant/log-determinant forms using Sylvester's identity.

### Phase-level coverage

Additional tests cover rank-1 inverse residuals, rank-1 log-determinant agreement, adaptive epsilon positivity, the Ricci-flow epsilon floor, topological output shape, quantum-state normalization, holographic dimensions, density-matrix Hermiticity/trace/positivity, and convergence bounds.

---

## Continuous Integration

GitHub Actions verifies Python 3.9–3.12. The workflow runs package installation, the complete pytest suite, Black formatting verification, and mypy static checking.

CI configuration is located at `.github/workflows/verify.yml`.

---

## Reproducibility

All engines that use randomized initialization accept a `seed` argument. The current implementations use NumPy's `default_rng` so experiments do not mutate the process-wide random state.

For reproducible experiments, record Python, NumPy, SciPy, operating-system, engine parameters, random seed, iteration count, and time step. Floating-point results can still vary across hardware, BLAS implementations, and library versions.

---

## Repository Structure

```text
RSHL-KERNEL/
├── .github/workflows/verify.yml
├── docs/MATHEMATICAL_FOUNDATIONS.md
├── rshl_kernel/
│   ├── __init__.py
│   ├── phase1_rank1.py
│   ├── phase2_rankk.py
│   ├── phase3_adaptive.py
│   ├── phase4_ricci_flow.py
│   ├── phase5_topology.py
│   ├── phase6_quantum.py
│   ├── phase7_holographic.py
│   ├── phase8_retrocausal.py
│   └── phase9_convergence.py
├── tests/
│   ├── __init__.py
│   ├── test_identities.py
│   └── test_phases.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## Engineering Standards

The repository is developed with these standards:

- preserve public APIs when practical;
- validate invalid numerical parameters early;
- keep exact identities separately testable;
- use deterministic RNGs for reproducible experiments;
- document numerical approximations explicitly;
- prefer low-rank operations over unnecessary dense inversions;
- test invariants, not only execution success;
- keep research claims proportional to implemented evidence.

See `CONTRIBUTING.md` for development guidance and `docs/MATHEMATICAL_FOUNDATIONS.md` for the detailed mathematical model.

---

## Research Interpretation

RSHL-KERNEL combines ideas from numerical linear algebra, differential geometry, topology, quantum dynamics, information theory, optimization, and holographic modeling.

The repository should be read at two levels:

1. **Implementation level:** what the code computes, which is directly testable.
2. **Interpretive level:** what those quantities may represent within the broader RSHL research program.

The implementation level is the appropriate basis for reproducible software verification. Stronger theoretical or physical conclusions require independent derivations, limiting-case analysis, numerical experiments, and—where applicable—empirical validation.

---

## License

**BSD 2-Clause License**.

The canonical license text is in `LICENSE`, and package metadata declares SPDX identifier `BSD-2-Clause`.

---

## Author

**Synthicsoft Labs**

Repository: https://github.com/SynthicsoftLabs/RSHL-KERNEL
Issues: https://github.com/SynthicsoftLabs/RSHL-KERNEL/issues
