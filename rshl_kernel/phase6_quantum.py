"""Phase 6: quantum-coherence dynamics on an evolving threshold graph."""

import time

import numpy as np
from scipy.linalg import expm
from scipy.spatial.distance import pdist, squareform


class QuantumTopologicalEngine:
    """Couple curvature adaptation, graph structure, and unitary state evolution."""

    def __init__(self, n=64, k=4, eps0=0.01, gamma=0.1, max_it=500,
                 dt=0.001, dt_quantum=0.05, seed=42):
        if n < 1 or k < 1 or k > n:
            raise ValueError("require 1 <= k <= n")
        if eps0 <= 0 or gamma < 0 or max_it < 0 or dt < 0 or dt_quantum < 0:
            raise ValueError("invalid evolution parameters")
        self.n, self.k = int(n), int(k)
        self.eps, self.gamma = float(eps0), float(gamma)
        self.max_it, self.dt, self.dt_quantum = int(max_it), float(dt), float(dt_quantum)
        self.history = []
        self.transitions = []
        self.rng = np.random.default_rng(seed)
        self.S = self.rng.standard_normal((self.n, self.k)) * 0.5
        psi = self.rng.standard_normal(self.n) + 1j * self.rng.standard_normal(self.n)
        self.psi = psi / np.linalg.norm(psi)

    def compute_curvature_proxy(self):
        return 4.0 * self.eps**2 * float(np.linalg.norm(self.S) ** 4)

    def ricci_adaptation_step(self):
        curvature = self.compute_curvature_proxy()
        self.eps = max(self.eps - self.gamma * curvature * self.dt, 1e-6)

    def get_graph_properties(self):
        """Build a median-threshold geometric graph and return adjacency/degrees."""
        distances = squareform(pdist(self.S))
        nonzero = distances[distances > 0]
        threshold = 0.0 if nonzero.size == 0 else np.percentile(nonzero, 50)
        threshold *= 1.0 + 2.0 * self.compute_curvature_proxy()
        adjacency = (distances <= threshold).astype(float)
        degrees = np.sum(adjacency, axis=1)
        return adjacency, degrees

    @staticmethod
    def build_hamiltonian(adjacency, degrees, curvature):
        """Construct the graph Hamiltonian used by the phase."""
        J = 2.0 * (1.0 + 5.0 * curvature)
        V = -10.0 * (degrees / np.max(degrees + 1e-6))
        return -J * adjacency + np.diag(V)

    def evolve_quantum_state(self, H):
        """Apply unitary matrix-exponential evolution and renormalize."""
        self.psi = expm(-1j * H * self.dt_quantum) @ self.psi
        self.psi /= np.linalg.norm(self.psi)

    def compute_quantum_metrics(self):
        """Return inverse participation ratio and phase coherence."""
        probabilities = np.abs(self.psi) ** 2
        ipr = float(np.sum(probabilities ** 2))
        phases = np.angle(self.psi)
        mean_cos = np.mean(np.cos(phases))
        mean_sin = np.mean(np.sin(phases))
        phase_coherence = float(np.sqrt(mean_cos**2 + mean_sin**2))
        return ipr, phase_coherence

    def run(self):
        """Execute coupled evolution and return quantum transition diagnostics."""
        start = time.perf_counter()
        previous_ipr = None

        for it in range(self.max_it):
            self.ricci_adaptation_step()
            curvature = self.compute_curvature_proxy()
            adjacency, degrees = self.get_graph_properties()
            H = self.build_hamiltonian(adjacency, degrees, curvature)
            self.evolve_quantum_state(H)
            ipr, phase_coherence = self.compute_quantum_metrics()
            self.S = self.S - self.dt * self.S

            if previous_ipr is not None:
                delta_ipr = abs(ipr - previous_ipr)
                if delta_ipr > 0.002:
                    self.transitions.append(
                        {"iter": it + 1, "curvature": curvature, "ipr": ipr,
                         "phase_coherence": phase_coherence, "delta_ipr": delta_ipr}
                    )
            previous_ipr = ipr

            if (it + 1) % 100 == 0:
                self.history.append(
                    {"iter": it + 1, "eps": self.eps, "curvature": curvature,
                     "ipr": ipr, "phase_coherence": phase_coherence}
                )

        return {"exec_time": time.perf_counter() - start,
                "milestones": self.history,
                "quantum_transitions": self.transitions}
