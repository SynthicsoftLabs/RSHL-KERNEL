# RSHL-TERRARIUM KERNEL

**Rivers State-Hamiltonian Learning Framework with Topological Evolution, Recursive Adaptation, and Manifold Integration**

[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD--2--Clause-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)
[![CI](https://github.com/SynthicsoftLabs/RSHL-KERNEL/actions/workflows/verify.yml/badge.svg)](https://github.com/SynthicsoftLabs/RSHL-KERNEL/actions/workflows/verify.yml)

---

## Overview

RSHL-KERNEL is a nine-phase mathematical and computational framework for low-rank metric evolution, adaptive state dynamics, curvature-driven parameter evolution, topological diagnostics, quantum-coherence modeling, holographic projection, boundary-to-bulk optimization, and identity convergence.

The framework is built as a progressive computational architecture. Each phase introduces a defined mathematical layer while retaining the independently callable engines of the preceding phases.

```text
Rank-1 Metric Structure
        │
        ▼
Rank-k Woodbury Structure
        │
        ▼
Adaptive Parameter Evolution
        │
        ▼
Curvature-Driven Evolution
        │
        ▼
Topological State Analysis
        │
        ▼
Quantum Graph Dynamics
        │
        ▼
Holographic Projection
        │
        ▼
Boundary-to-Bulk Optimization
        │
        ▼
Identity Convergence
```

---

## Nine-Phase Architecture

| Phase | Engine | Computational Layer |
|---|---|---|
| 1 | `SingularityEngine` | Rank-1 metric and Sherman-Morrison structure |
| 2 | `WoodburyEngine` | Rank-k metric and Woodbury structure |
| 3 | `AdaptiveWoodburyEngine` | State-dependent metric parameterization |
| 4 | `RicciFlowWoodburyEngine` | Curvature-driven metric adaptation |
| 5 | `TopologicalRicciFlowEngine` | Threshold-graph topology analysis |
| 6 | `QuantumTopologicalEngine` | Quantum state evolution on dynamic graphs |
| 7 | `HolographicProjectionEngine` | Bulk-to-boundary projection |
| 8 | `RetrocausalHolographicEngine` | Boundary-to-bulk adjoint optimization |
| 9 | `IdentityConvergenceEngine` | Spherical convergence and information diagnostics |

Every engine is exported directly from `rshl_kernel`.

---

## Mathematical Foundation

### Phase 1 — Rank-1 Metric

For \(s\in\mathbb{R}^n\):

\[
G=I_n+\varepsilon ss^T.
\]

The exact inverse is

\[
G^{-1}=I_n-\frac{\varepsilon}{1+\varepsilon s^Ts}ss^T.
\]

The determinant and log-determinant are

\[
\det(G)=1+\varepsilon s^Ts,
\qquad
\log\det(G)=\log(1+\varepsilon s^Ts).
\]

### Phase 2 — Rank-k Woodbury Metric

For \(S\in\mathbb{R}^{n\times k}\):

\[
G=I_n+\varepsilon SS^T.
\]

The exact Woodbury inverse is

\[
G^{-1}=I_n-\varepsilon S(I_k+\varepsilon S^TS)^{-1}S^T.
\]

Sylvester's determinant identity gives

\[
\det(I_n+\varepsilon SS^T)=\det(I_k+\varepsilon S^TS).
\]

The nontrivial solve therefore operates in the \(k\times k\) system. When \(k\ll n\), the low-rank representation provides the principal computational reduction.

### Phase 3 — Adaptive Metric Parameter

\[
\varepsilon(S)=\frac{\varepsilon_0}{1+\alpha\|S\|_F^2}.
\]

The engine exposes the adaptive parameter and its configured sensitivity/gradient quantity.

### Phase 4 — Curvature Evolution

\[
\mathcal{R}_{proxy}=4\varepsilon^2\|S\|_F^4.
\]

\[
\varepsilon_{t+1}=\max\left(\varepsilon_t-\gamma\mathcal{R}_{proxy}\Delta t,10^{-6}\right).
\]

### Phase 5 — Topological Evolution

Rows of the evolving state matrix are embedded as points in Euclidean space. Pairwise distances generate threshold graphs at the 10th, 25th, 50th, 75th, and 90th percentiles.

The engine computes connected components \(\beta_0\), the graph-cycle quantity \(\beta_1=E-N+C\), and the configured \(\beta_2\) extension point. Topology transitions are recorded across the sampled filtration.

### Phase 6 — Quantum Topological Dynamics

\[
H=-JA+\operatorname{diag}(V),
\]

with

\[
J=2(1+5\mathcal{R}_{proxy}),
\qquad
V_i=-10\frac{d_i}{\max_j(d_j+10^{-6})}.
\]

The complex state evolves through

\[
\psi_{t+1}=e^{-iH\Delta t_q}\psi_t.
\]

The engine records inverse participation ratio, phase coherence, curvature, adaptive epsilon, and transition events.

### Phase 7 — Holographic Projection

A normalized bulk state generates a rank-1 bulk projector. The projector is expanded to the boundary through Kronecker-product upscaling and coupled into the boundary representation.

The engine computes bulk coherence, boundary entropy, and Fourier-spectrum fractal-dimension diagnostics.

### Phase 8 — Boundary-to-Bulk Optimization

The target boundary field defines

\[
L=B-B_{target}.
\]

The boundary gradient is mapped into bulk matrix space through the reverse projection. The density matrix is symmetrized, spectrally projected onto the positive-semidefinite cone, and trace-normalized.

The engine records boundary loss before and after optimization, bulk entropy, and optimization ratio.

### Phase 9 — Identity Convergence

For normalized system and reference states,

\[
a=\langle s,r\rangle,
\qquad
\omega=\arccos(a).
\]

The state update uses spherical linear interpolation:

\[
s(t)=\frac{\sin((1-t)\omega)}{\sin\omega}s_0+\frac{\sin(t\omega)}{\sin\omega}r.
\]

The engine records alignment, probability-space relative entropy, temporal-dilation proxy, and final convergence metrics.

---

## Installation

```bash
pip install -e .
```

Development environment:

```bash
pip install -e ".[dev]"
```

Runtime dependencies: NumPy >= 1.24 and SciPy >= 1.10.

Development tooling: pytest, Black, and mypy.

Python 3.9–3.12 are configured in continuous integration.

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

### Complete Nine-Phase Execution

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
phase7 = HolographicProjectionEngine().execute()
phase8 = RetrocausalHolographicEngine().execute()
phase9 = IdentityConvergenceEngine().run()
```

---

## Verification

Run the complete suite:

```bash
pytest -v
```

Coverage includes Woodbury and Sylvester identities, rank-1 residuals, log-determinants, adaptive epsilon, Ricci epsilon bounds, topological output structure, quantum normalization, holographic dimensions, density-matrix Hermiticity/trace/positivity, and convergence bounds.

---

## Continuous Integration

GitHub Actions executes the verification pipeline across Python 3.9–3.12.

The workflow performs repository checkout, environment provisioning, dependency installation, package installation, the complete test suite, Black verification, and mypy analysis.

Workflow: `.github/workflows/verify.yml`

---

## Reproducibility

All stochastic engines accept `seed` and use NumPy's `default_rng` for isolated deterministic initialization.

Record Python, NumPy, SciPy, operating system, engine parameters, random seed, iteration count, time step, hardware, and numerical backend for reproducible experiments.

---

## Computational Complexity

The rank-k Woodbury formulation moves the nontrivial solve into a \(k\times k\) system. The low-rank representation is most efficient when \(k\ll n\).

The public `woodbury_inverse()` method returns a dense \(n\times n\) matrix and therefore uses \(O(n^2)\) storage and matrix formation. Factorized downstream operations preserve the low-rank computational structure and avoid dense materialization.

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

## Engineering Principles

- Preserve the nine-phase architecture.
- Keep public engine names stable.
- Validate numerical parameters at construction time.
- Use exact closed-form identities where available.
- Keep mathematical identities independently testable.
- Use isolated seeded random generators.
- Preserve low-rank structure through downstream operations.
- Test numerical invariants directly.
- Document mathematical quantities and computational transformations.
- Separate definitions, algorithms, diagnostics, and experimental parameters by explicit sectioning.

---

## Documentation

| Document | Purpose |
|---|---|
| `README.md` | Architecture, installation, usage, mathematics, verification |
| `docs/MATHEMATICAL_FOUNDATIONS.md` | Detailed nine-phase mathematical specification |
| `CONTRIBUTING.md` | Development workflow |
| `CHANGELOG.md` | Version history |
| `LICENSE` | BSD 2-Clause License |

---

## License

**BSD 2-Clause License**

The canonical license text is contained in `LICENSE`. Package metadata declares `BSD-2-Clause`.

---

## Author

**Synthicsoft Labs**

Repository: https://github.com/SynthicsoftLabs/RSHL-KERNEL
Issues: https://github.com/SynthicsoftLabs/RSHL-KERNEL/issues
