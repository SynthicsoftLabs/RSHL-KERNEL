"""Phase 1: rank-1 metric evolution and closed-form verification.

The engine constructs the rank-1 metric

    G = I + epsilon * s s^T

and evaluates its inverse and log-determinant using the
Sherman-Morrison / matrix-determinant-lemma forms rather than dense inversion.
"""

import time

import numpy as np
from scipy.linalg import eigvals


class SingularityEngine:
    """Evolve and inspect a rank-1 positive-definite metric."""

    def __init__(self, dim=16, epsilon=0.01, max_iterations=500, seed=None):
        if dim < 1:
            raise ValueError("dim must be positive")
        if epsilon <= 0:
            raise ValueError("epsilon must be positive")
        if max_iterations < 0:
            raise ValueError("max_iterations must be non-negative")

        self.dim = int(dim)
        self.epsilon = float(epsilon)
        self.max_iterations = int(max_iterations)
        self.iterations = 0
        self.history = []
        self.rng = np.random.default_rng(seed)
        self.state = self.rng.standard_normal(self.dim) * 0.1

    def metric(self):
        """Return the dense metric matrix G = I + epsilon*s*s^T."""
        return np.eye(self.dim) + self.epsilon * np.outer(self.state, self.state)

    def metric_inverse_closed_form(self):
        """Return G^-1 using the exact rank-1 Sherman-Morrison form."""
        s = self.state
        s_norm_sq = float(np.dot(s, s))
        coeff = self.epsilon / (1.0 + self.epsilon * s_norm_sq)
        return np.eye(self.dim) - coeff * np.outer(s, s)

    def logdet_metric_closed_form(self):
        """Return log(det(G)) using the matrix determinant lemma."""
        s_norm_sq = float(np.dot(self.state, self.state))
        return float(np.log(1.0 + self.epsilon * s_norm_sq))

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

    def evolve_state(self, dt=0.001):
        """Apply the current exponential-decay discretization to the state."""
        if dt < 0:
            raise ValueError("dt must be non-negative")
        self.state = self.state - dt * self.state

    def execute_phase_transition(self):
        """Execute the configured evolution and return milestone diagnostics."""
        start_time = time.perf_counter()

        for _ in range(self.max_iterations):
            G_inv = self.metric_inverse_closed_form()
            scale = 1.0 + 0.001 * self.iterations
            A = -scale * G_inv

            lambda_max_real = self.max_real_part(A)
            rho = self.spectral_radius(A)

            self.evolve_state(dt=0.001)
            self.iterations += 1

            if self.iterations % 100 == 0:
                self.history.append(
                    {
                        "iter": self.iterations,
                        "dim": self.dim,
                        "lambda_max_real": lambda_max_real,
                        "spectral_radius": rho,
                        "entropy_proxy": 0.5 * self.logdet_metric_closed_form(),
                    }
                )

        final_G_inv = self.metric_inverse_closed_form()
        final_scale = 1.0 + 0.001 * self.iterations
        final_A = -final_scale * final_G_inv

        return {
            "execution_time_sec": time.perf_counter() - start_time,
            "final_lambda_max_real": self.max_real_part(final_A),
            "final_spectral_radius": self.spectral_radius(final_A),
            "final_entropy_proxy": 0.5 * self.logdet_metric_closed_form(),
            "total_iterations": self.iterations,
            "milestones": self.history,
        }
