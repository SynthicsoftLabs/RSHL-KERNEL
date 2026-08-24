"""Phase 2: rank-k Woodbury metric evolution.

For G = I_n + epsilon*S*S^T, the implementation evaluates the exact inverse
through the k-dimensional Woodbury system instead of an n-dimensional dense
inverse.  The phase also records determinant, entropy, spectral, and gradient
proxies for reproducible numerical experiments.
"""

import time

import numpy as np
from scipy.linalg import eigvals


class WoodburyEngine:
    """Run rank-k Woodbury metric evolution and collect diagnostics."""

    def __init__(self, n=64, k=4, eps=0.01, max_it=500, dt=0.001, seed=None):
        if n < 1 or k < 1:
            raise ValueError("n and k must be positive")
        if eps <= 0:
            raise ValueError("eps must be positive")
        if max_it < 0:
            raise ValueError("max_it must be non-negative")
        if dt < 0:
            raise ValueError("dt must be non-negative")
        if k > n:
            raise ValueError("k cannot exceed n for the configured state matrix")

        self.n = int(n)
        self.k = int(k)
        self.eps = float(eps)
        self.max_it = int(max_it)
        self.dt = float(dt)
        self.history = []
        self.rng = np.random.default_rng(seed)
        self.S = self.rng.standard_normal((self.n, self.k)) * 0.1

    def _inner_system(self):
        """Return the k-by-k Woodbury inner system."""
        return np.eye(self.k) + self.eps * self.S.T @ self.S

    def woodbury_inverse(self):
        """Return the exact inverse of I + eps*S*S^T via Woodbury."""
        inner = self._inner_system()
        return np.eye(self.n) - self.eps * self.S @ np.linalg.solve(inner, self.S.T)

    def logdet(self):
        """Return log(det(I + eps*S*S^T)) using Sylvester's identity."""
        sign, logdet = np.linalg.slogdet(self._inner_system())
        if sign <= 0:
            raise np.linalg.LinAlgError("Woodbury inner system is not positive definite")
        return float(logdet)

    def entropy_gradient(self):
        """Return the rank-k entropy-gradient proxy used by this phase."""
        inner = self._inner_system()
        return self.eps * self.S @ np.linalg.solve(inner, np.eye(self.k))

    @staticmethod
    def spectral_radius(A):
        """Return max(|lambda|) over the eigenvalues of A."""
        ev = eigvals(A)
        return float(np.max(np.abs(ev)))

    @staticmethod
    def max_real_part(A):
        """Return the largest real component of the eigenvalues of A."""
        ev = eigvals(A)
        return float(np.max(np.real(ev)))

    def evolve_state(self):
        """Advance S by the configured explicit decay step."""
        self.S = self.S - self.dt * self.S

    def run(self):
        """Execute the configured iterations and return milestone diagnostics."""
        start = time.perf_counter()

        for it in range(self.max_it):
            G_inv = self.woodbury_inverse()
            scale = 1.0 + 0.001 * it
            A = -scale * G_inv

            rho = self.spectral_radius(A)
            lam_max_real = self.max_real_part(A)
            entropy_proxy = 0.5 * self.logdet()

            self.evolve_state()
            grad_norm = float(np.linalg.norm(self.entropy_gradient()))

            if (it + 1) % 100 == 0:
                self.history.append(
                    {
                        "iter": it + 1,
                        "lambda_max_real": lam_max_real,
                        "rho": rho,
                        "entropy_proxy": entropy_proxy,
                        "grad_norm": grad_norm,
                    }
                )

        return {
            "exec_time": time.perf_counter() - start,
            "milestones": self.history,
        }
