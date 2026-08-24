# RSHL-TERRARIUM KERNEL

**Rivers State-Hamiltonian Learning Framework with Topological Evolution, Recursive Adaptation, and Manifold Integration**

A complete mathematical framework for high-dimensional metric evolution, topological phase detection, quantum coherence modeling, and holographic projection systems.

---

## Overview

The RSHL-TERRARIUM KERNEL implements a progressive mathematical framework spanning:

- **Rank-k Woodbury metric evolution** with exact closed-form identities
- **Discrete Ricci flow** for curvature-driven metric adaptation
- **Persistent homology** for topological phase transition detection
- **Quantum coherence** integration on dynamic graphs
- **Holographic projection** via AdS/CFT-inspired bulk-to-boundary mapping
- **Retrocausal optimization** through adjoint backpropagation
- **Identity convergence** via spherical linear interpolation

All implementations use exact mathematical identities (Woodbury, Sylvester, Sherman-Morrison) to achieve O(k³ + nk²) computational complexity instead of O(n³).

---

## Installation

```bash
pip install -e .
```

Or with development dependencies:

```bash
pip install -e ".[dev]"
```

---

## Usage

```python
from rshl_kernel import WoodburyEngine

engine = WoodburyEngine(n=64, k=4, eps=0.01, max_it=500, seed=42)
result = engine.run()

print(f"Execution Time: {result['exec_time']:.4f}s")
print(f"Final Spectral Radius: {result['milestones'][-1]['rho']:.6f}")
```

---

## Mathematical Foundations

### Core Identity: Woodbury Matrix Formula

For a state matrix S ∈ ℝ^(n×k) and metric parameter ε > 0:

G = I_n + εSS^T

**Exact Inverse (Woodbury Identity):**
G⁻¹ = I_n - εS(I_k + εS^TS)⁻¹S^T

**Exact Determinant (Sylvester Identity):**
det(G) = det(I_k + εS^TS)

---

## Testing

Run the mathematical identity verification suite:

```bash
pytest tests/ -v
```

---

## License

MIT

---

## Author

Synthicsoft Labs
