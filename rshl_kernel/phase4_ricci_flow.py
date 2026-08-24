"""Phase 4: curvature-driven adaptation of the Woodbury metric."""

import time

import numpy as np
from scipy.linalg import eigvals


class RicciFlowWoodburyEngine:
    """Combine low-rank metric evolution with a scalar curvature proxy."""

    def __init__(self, n=64, k=4, eps0=0.01, gamma=0.1, max_it=500, dt=0.001, seed=42):
        if n < 1 or k < 1 or k > n:
            raise ValueError("require 1 <= k <= n")
        if eps0 <= 0 or gamma < 0 or max_it < 0 or dt < 0:
            raise ValueError("eps0 must be positive; gamma, max_it and dt must be non-negative")
        self.n, self.k = int(n), int(k)
        self.eps, self.gamma = float(eps0), float(gamma)
        self.max_it, self.dt = int(max_it), float(dt)
        self.history = []
        self.rng = np.random.default_rng(seed)
        self.S = self.rng.standard_normal((self.n, self.k)) * 0.5

    def compute_curvature_proxy(self):
        """Return the phase's scalar curvature proxy."""
        s_norm_sq = float(np.linalg.norm(self.S) ** 2)
        return 4.0 * self.eps**2 * s_norm_sq**2

    def ricci_adaptation_step(self):
        """Apply the configured explicit curvature-driven epsilon update."""
        curvature = self.compute_curvature_proxy()
        self.eps = max(self.eps - self.gamma * curvature * self.dt, 1e-6)

    def woodbury_inverse(self):
        """Return the exact low-rank metric inverse."""
        inner = np.eye(self.k) + self.eps * self.S.T @ self.S
        return np.eye(self.n) - self.eps * self.S @ np.linalg.solve(inner, self.S.T)

    @staticmethod
    def spectral_radius(A):
        return float(np.max(np.abs(eigvals(A))))

    @staticmethod
    def max_real_part(A):
        return float(np.max(np.real(eigvals(A))))

    def run(self):
        """Execute curvature adaptation and return milestone diagnostics."""
        start_time = time.perf_counter()
        for it in range(self.max_it):
            self.ricci_adaptation_step()
            curvature = self.compute_curvature_proxy()
            G_inv = self.woodbury_inverse()
            scale = 1.0 + 0.001 * it
            A = -scale * G_inv
            rho = self.spectral_radius(A)
            lam_max_real = self.max_real_part(A)

            inner = np.eye(self.k) + self.eps * self.S.T @ self.S
            sign, logdet = np.linalg.slogdet(inner)
            if sign <= 0:
                raise np.linalg.LinAlgError("Ricci-flow inner system is not positive definite")
            entropy = 0.5 * logdet
            self.S = self.S - self.dt * self.S

            if (it + 1) % 100 == 0:
                self.history.append(
                    {"iter": it + 1, "eps": self.eps, "curvature": curvature,
                     "rho": rho, "lam_max": lam_max_real, "entropy": float(entropy)}
                )

        return {"exec_time": time.perf_counter() - start_time, "milestones": self.history}
