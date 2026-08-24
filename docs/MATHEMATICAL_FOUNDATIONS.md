# RSHL-KERNEL Mathematical Foundations

## Purpose

RSHL-KERNEL is organized as a progressive nine-phase numerical framework. Each phase builds a computational layer on the state representation established by earlier phases while retaining independently callable engines.

The repository contains both exact linear-algebra identities and deliberately approximate diagnostic models. Exact identities should be distinguished from modeling choices, numerical proxies, and research hypotheses.

## Phase 1 — Rank-1 Metric

The canonical metric is

\[
G = I_n + \varepsilon ss^T.
\]

For a scalar rank-1 update, Sherman-Morrison gives

\[
G^{-1} = I_n - \frac{\varepsilon}{1+\varepsilon s^Ts}ss^T.
\]

The matrix determinant lemma gives

\[
\det(G)=1+\varepsilon s^Ts,
\qquad
\log\det(G)=\log(1+\varepsilon s^Ts).
\]

The implementation uses these closed forms rather than a dense matrix inverse.

## Phase 2 — Rank-k Woodbury Metric

Let \(S\in\mathbb{R}^{n\times k}\). The metric becomes

\[
G=I_n+\varepsilon SS^T.
\]

The Woodbury identity gives the exact inverse

\[
G^{-1}=I_n-\varepsilon S(I_k+\varepsilon S^TS)^{-1}S^T.
\]

Sylvester's determinant identity gives

\[
\det(I_n+\varepsilon SS^T)
=
\det(I_k+\varepsilon S^TS).
\]

This moves the nontrivial inversion from an \(n\times n\) system to a \(k\times k\) system. For \(k\ll n\), this is the central computational advantage of the framework.

## Phase 3 — Adaptive Regularization

The effective metric parameter is state-dependent:

\[
\varepsilon(S)=\frac{\varepsilon_0}{1+\alpha\|S\|_F^2}.
\]

As the state norm grows, the effective perturbation is reduced. The implementation also exposes the configured sensitivity/gradient proxy used by the phase's diagnostic output.

## Phase 4 — Curvature-Driven Adaptation

The current phase defines a scalar curvature proxy

\[
\mathcal{R}_{proxy}=4\varepsilon^2\|S\|_F^4.
\]

The explicit adaptation step is

\[
\varepsilon_{t+1}
=
\max\left(\varepsilon_t-\gamma\,\mathcal{R}_{proxy}\,\Delta t,10^{-6}\right).
\]

This is a discrete numerical adaptation rule. It should not be interpreted as a complete implementation of the tensorial Ricci-flow equation without additional geometric structure.

## Phase 5 — Topological Diagnostics

The state rows are treated as points in a Euclidean embedding. Pairwise distances define threshold graphs over a five-threshold filtration using the 10th, 25th, 50th, 75th, and 90th percentiles.

The implementation computes a connected-component estimate \(\beta_0\), a graph-cycle estimate

\[
\beta_1 \approx E-N+C,
\]

and retains a \(\beta_2\) extension hook. The current \(\beta_2\) approximation reports zero rather than claiming a full higher-dimensional persistent-homology calculation.

A transition is recorded when the full tuple sequence changes between sampled thresholds.

## Phase 6 — Quantum-Coherence Layer

The evolving point cloud induces a median-distance threshold graph. A Hamiltonian is constructed as

\[
H=-J A+\operatorname{diag}(V),
\]

with

\[
J=2(1+5\mathcal{R}_{proxy}),
\qquad
V_i=-10\frac{d_i}{\max_j(d_j+10^{-6})}.
\]

The normalized complex state is evolved using

\[
\psi_{t+1}=e^{-iH\Delta t_q}\psi_t.
\]

The phase reports inverse participation ratio (IPR)

\[
\mathrm{IPR}=\sum_i |\psi_i|^4
\]

and a circular phase-coherence measure based on mean sine and cosine components.

## Phase 7 — Holographic Projection

A normalized complex bulk state is converted into a rank-1 bulk projector and expanded to the boundary through a Kronecker-product upscaling. The boundary state is coupled toward that projection with a fixed coupling strength.

The phase reports:

- bulk coherence,
- von Neumann entropy of a normalized boundary Gram matrix,
- a Fourier-spectrum scaling estimate used as an emergent fractal-dimension proxy.

These are numerical constructions inspired by holographic language; they are not, by themselves, a physical derivation of AdS/CFT correspondence.

## Phase 8 — Retrocausal / Adjoint Optimization

The boundary objective defines an error matrix

\[
L=B-B_{target}.
\]

The boundary gradient is mapped back to bulk matrix space through the reverse projection operator. The bulk density matrix is then projected back onto the Hermitian positive-semidefinite, trace-normalized state space.

The phase records before/after boundary loss, bulk entropy, and optimization ratio. The term "retrocausal" describes the direction of objective propagation in the framework; the implementation is a conventional numerical optimization procedure and does not establish physical backward causation.

## Phase 9 — Identity Convergence

The final phase compares a normalized system state with a normalized reference state. Alignment is

\[
a=\langle s,r\rangle,
\]

and the angular separation is

\[
\omega=\arccos(a).
\]

The update uses spherical linear interpolation (SLERP):

\[
s(t)=
\frac{\sin((1-t)\omega)}{\sin\omega}s_0
+
\frac{\sin(t\omega)}{\sin\omega}r.
\]

The implementation additionally reports a probability-space relative-entropy diagnostic and a temporal-dilation proxy \(1-a\).

## Numerical Verification Principles

1. Compare closed-form identities against dense reference calculations at controlled dimensions.
2. Use fixed random seeds when reproducibility is required.
3. Track residuals rather than only boolean pass/fail results.
4. Separate mathematical identity tests from model-behavior tests.
5. Treat topology, curvature, holographic, retrocausal, and convergence quantities as the definitions implemented by this repository unless a stronger mathematical derivation is supplied.
6. Record environment and dependency versions for reproducible research.

## Complexity

For the rank-k metric, the expensive nontrivial linear solve operates in k dimensions. Forming the dense n-by-n inverse representation still requires O(n^2) storage/work because the public API returns that matrix. The Woodbury identity therefore provides its strongest asymptotic advantage when downstream operations can exploit the factorized low-rank representation rather than materializing the full inverse.

This distinction is important: the identity itself reduces the inversion problem from an n-dimensional solve to a k-dimensional solve, while a dense returned matrix can reintroduce O(n^2) materialization costs.
