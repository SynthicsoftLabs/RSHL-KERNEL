"""Phase 5: topological diagnostics on the evolving low-rank state.

The implementation uses distance-threshold graph filtrations and lightweight
Betti-number proxies.  It is intentionally an approximation rather than a
claim of full persistent-homology computation; the API preserves the original
transition-detection workflow.
"""

import time

import numpy as np
from scipy.linalg import eigvals
from scipy.spatial.distance import pdist, squareform


class TopologicalRicciFlowEngine:
    """Combine curvature adaptation with graph-topology diagnostics."""

    def __init__(self, n=64, k=4, eps0=0.01, gamma=0.1, max_it=500, dt=0.001, seed=42):
        if n < 1 or k < 1 or k > n:
            raise ValueError("require 1 <= k <= n")
        if eps0 <= 0 or gamma < 0 or max_it < 0 or dt < 0:
            raise ValueError("invalid evolution parameters")
        self.n, self.k = int(n), int(k)
        self.eps, self.gamma = float(eps0), float(gamma)
        self.max_it, self.dt = int(max_it), float(dt)
        self.history = []
        self.topological_transitions = []
        self.rng = np.random.default_rng(seed)
        self.S = self.rng.standard_normal((self.n, self.k)) * 0.5

    def compute_curvature_proxy(self):
        s_norm_sq = float(np.linalg.norm(self.S) ** 2)
        return 4.0 * self.eps**2 * s_norm_sq**2

    def ricci_adaptation_step(self):
        curvature = self.compute_curvature_proxy()
        self.eps = max(self.eps - self.gamma * curvature * self.dt, 1e-6)

    def woodbury_inverse(self):
        inner = np.eye(self.k) + self.eps * self.S.T @ self.S
        return np.eye(self.n) - self.eps * self.S @ np.linalg.solve(inner, self.S.T)

    @staticmethod
    def _count_connected_components(adjacency):
        n = adjacency.shape[0]
        visited = np.zeros(n, dtype=bool)
        components = 0
        for i in range(n):
            if not visited[i]:
                components += 1
                queue = [i]
                visited[i] = True
                while queue:
                    node = queue.pop(0)
                    for neighbor in np.where(adjacency[node] == 1)[0]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
        return components

    def _estimate_loops(self, adjacency):
        n = adjacency.shape[0]
        edges = int(np.sum(adjacency) // 2)
        components = self._count_connected_components(adjacency)
        return max(0, edges - n + components)

    @staticmethod
    def _estimate_voids(adjacency, points, threshold):
        # Kept as an explicit API hook for higher-order complex estimators.
        # The current lightweight approximation reports no beta_2 features.
        del adjacency, points, threshold
        return 0

    def compute_persistent_homology_approx(self):
        """Return approximate Betti tuples over five distance thresholds."""
        distances = squareform(pdist(self.S))
        nonzero = distances[distances > 0]
        if nonzero.size == 0:
            return [(self.n, 0, 0)] * 5

        betti_numbers = []
        for threshold in np.percentile(nonzero, [10, 25, 50, 75, 90]):
            adjacency = (distances <= threshold).astype(int)
            beta_0 = self._count_connected_components(adjacency)
            beta_1 = self._estimate_loops(adjacency)
            beta_2 = self._estimate_voids(adjacency, self.S, threshold)
            betti_numbers.append((beta_0, beta_1, beta_2))
        return betti_numbers

    @staticmethod
    def detect_topological_transition(current_betti, prev_betti):
        return prev_betti is not None and current_betti != prev_betti

    @staticmethod
    def spectral_radius(A):
        return float(np.max(np.abs(eigvals(A))))

    @staticmethod
    def max_real_part(A):
        return float(np.max(np.real(eigvals(A))))

    def run(self):
        """Execute evolution and record topology changes and milestones."""
        start = time.perf_counter()
        previous_betti = None
        current_betti = None

        for it in range(self.max_it):
            self.ricci_adaptation_step()
            curvature = self.compute_curvature_proxy()
            A = -(1.0 + 0.001 * it) * self.woodbury_inverse()
            rho = self.spectral_radius(A)
            lam_max = self.max_real_part(A)

            inner = np.eye(self.k) + self.eps * self.S.T @ self.S
            sign, logdet = np.linalg.slogdet(inner)
            if sign <= 0:
                raise np.linalg.LinAlgError("topological inner system is not positive definite")
            entropy = 0.5 * logdet

            if (it + 1) % 10 == 0:
                current_betti = self.compute_persistent_homology_approx()
                if self.detect_topological_transition(current_betti, previous_betti):
                    self.topological_transitions.append(
                        {"iter": it + 1, "curvature": curvature,
                         "betti_change": current_betti, "prev_betti": previous_betti}
                    )
                previous_betti = current_betti

            self.S = self.S - self.dt * self.S

            if (it + 1) % 100 == 0:
                self.history.append(
                    {"iter": it + 1, "eps": self.eps, "curvature": curvature,
                     "rho": rho, "lam_max": lam_max, "entropy": float(entropy),
                     "betti": current_betti}
                )

        return {"exec_time": time.perf_counter() - start,
                "milestones": self.history,
                "topological_transitions": self.topological_transitions}
