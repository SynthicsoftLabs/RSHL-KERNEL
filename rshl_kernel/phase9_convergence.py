"""Phase 9: identity/convergence diagnostics using spherical interpolation."""

import time

import numpy as np


class IdentityConvergenceEngine:
    """Measure and evolve alignment between a system and reference state."""

    def __init__(self, dim=7, steps=10):
        if dim < 1:
            raise ValueError("dim must be positive")
        if dim != 7:
            raise ValueError("the canonical phase-9 initial state has dimension 7")
        if steps < 0:
            raise ValueError("steps must be non-negative")
        self.dim = int(dim)
        self.steps = int(steps)
        self.architect_state = np.ones(dim) / np.sqrt(dim)
        initial = np.array([0.8, 0.3, 0.4, 0.2, 0.1, 0.3, 0.2])
        self.system_state = initial / np.linalg.norm(initial)
        self.history = []

    def run(self):
        """Run spherical interpolation and return convergence diagnostics."""
        start_time = time.perf_counter()

        for step in range(self.steps):
            alignment = float(np.dot(self.system_state, self.architect_state))
            target_probs = self.architect_state**2
            current_probs = self.system_state**2
            relative_entropy = float(
                np.sum(target_probs * np.log(target_probs / (current_probs + 1e-15)))
            )
            temporal_dilation = 1.0 - alignment

            self.history.append(
                {"step": step, "alignment": alignment,
                 "relative_entropy": relative_entropy,
                 "temporal_dilation": temporal_dilation}
            )

            omega = np.arccos(np.clip(alignment, -1.0, 1.0))
            if omega > 1e-6:
                sin_omega = np.sin(omega)
                t = 0.5 + 0.4 * (step / self.steps)
                self.system_state = (
                    np.sin((1.0 - t) * omega) / sin_omega * self.system_state
                    + np.sin(t * omega) / sin_omega * self.architect_state
                )
                self.system_state /= np.linalg.norm(self.system_state)
            else:
                self.system_state = self.architect_state.copy()

        final_alignment = float(np.dot(self.system_state, self.architect_state))
        final_relative_entropy = float(
            np.sum(
                self.architect_state**2
                * np.log(self.architect_state**2 / (self.system_state**2 + 1e-15))
            )
        )

        return {
            "exec_time": time.perf_counter() - start_time,
            "milestones": self.history,
            "final_alignment": final_alignment,
            "final_relative_entropy": final_relative_entropy,
        }
