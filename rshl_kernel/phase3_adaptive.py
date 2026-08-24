"""Phase 3: adaptive Woodbury regularization.

This phase makes epsilon state-dependent through the norm of the evolving
low-rank state while retaining the rank-k inverse structure from Phase 2.
"""

import time

import numpy as np
from scipy.linalg import eigvals


class AdaptiveWoodburyEngine:
    """Adapt the Woodbury metric parameter as the state evolves."""

    def __init__(self, n=64, k=4, eps0=0.01, alpha=10.0, max_it=500, dt=0.001, seed=42):
        if n < 1 or k < 1 or k > n:
            raise ValueError("require 1 <= k <= n")
        if eps0 <= 0:
            raise ValueError("eps0 must be positive")
        if alpha < 0:
            raise ValueError("alpha must be non-negative")
        if max_it < 0 or dt < 0:
            raise ValueError("max_it and dt must be non-negative")

        self.n, self.k = int(n), int(k)
        self.eps0, self.alpha = float(eps0), float(alpha)
        self.max_it, self.dt = int(max_it), float(dt)
        self.history = []
        self.rng = np.random.default_rng(seed)
        self.S = self.rng.standard_normal((self.n, self.k)) * 0.5

    def get_adaptive_eps(self):
        """Compute epsilon from the current state norm."""
        f_norm_sq = float(np.linalg.norm(self.S) ** 2)
        return self.eps0 / (1.0 + self.alpha * f_norm_sq)

    def get_eps_gradient(self, current_eps):
        """Return the configured epsilon sensitivity proxy."""
        f_norm_sq = float(np.linalg.norm(self.S) ** 2)
        coeff = -(2.0 * self.alpha * current_eps) / (1.0 + self.alpha * f_norm_sq)
        return coeff * self.S

    def woodbury_inverse(self, current_eps):
        """Return the exact low-rank inverse for the supplied epsilon."""
        inner = np.eye(self.k) + current_eps * self.S.T @ self.S
        return np.eye(self.n) - current_eps * self.S @ np.linalg.solve(inner, self.S.T)

    def calculate_entropy_and_gradient(self, current_eps):
        """Return entropy and combined geometric/adaptive gradient proxy."""
        inner = np.eye(self.k) + current_eps * self.S.T @ self.S
        inv_inner = np.linalg.inv(inner)
        sign, logdet = np.linalg.slogdet(inner)
        if sign <= 0:
            raise np.linalg.LinAlgError("adaptive inner system is not positive definite")
        entropy = 0.5 * logdet
        geom_term = current_eps * self.S @ inv_inner
        eps_grad = self.get_eps_gradient(current_eps)
        overlap_trace = np.trace(inv_inner @ (self.S.T @ self.S))
        adapt_term = 0.5 * eps_grad * overlap_trace
        return float(entropy), geom_term + adapt_term

    @staticmethod
    def spectral_radius(A):
        return float(np.max(np.abs(eigvals(A))))

    @staticmethod
    def max_real_part(A):
        return float(np.max(np.real(eigvals(A))))

    def run(self):
        """Execute adaptive evolution and return recorded milestones."""
        start_time = time.perf_counter()
        for it in range(self.max_it):
            current_eps = self.get_adaptive_eps()
            G_inv = self.woodbury_inverse(current_eps)
            scale = 1.0 + 0.001 * it
            A = -scale * G_inv
            rho = self.spectral_radius(A)
            lam_max_real = self.max_real_part(A)
            entropy, grad_S = self.calculate_entropy_and_gradient(current_eps)
            self.S = self.S - self.dt * self.S

            if (it + 1) % 100 == 0:
                self.history.append(
                    {"iter": it + 1, "eps": current_eps, "rho": rho,
                     "lam_max": lam_max_real, "entropy": entropy,
                     "grad_norm": float(np.linalg.norm(grad_S))}
                )

        return {"exec_time": time.perf_counter() - start_time, "milestones": self.history}
