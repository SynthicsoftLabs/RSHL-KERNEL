"""Phase 8: adjoint-style holographic optimization.

The term ``retrocausal`` names the framework's optimization interpretation:
future/boundary objectives are propagated back into the bulk representation.
This implementation is a numerical optimization model, not a claim of
experimentally demonstrated backward physical causation.
"""

import time

import numpy as np


class RetrocausalHolographicEngine:
    """Optimize a bulk density matrix against a prescribed boundary target."""

    def __init__(self, bulk_dim=32, boundary_size=64, seed=None):
        if bulk_dim < 1 or boundary_size < 1:
            raise ValueError("bulk_dim and boundary_size must be positive")
        if boundary_size % bulk_dim != 0:
            raise ValueError("boundary_size must be divisible by bulk_dim")
        self.bulk_dim = int(bulk_dim)
        self.boundary_size = int(boundary_size)
        self.scale = self.boundary_size // self.bulk_dim
        self.rng = np.random.default_rng(seed)

        x = np.linspace(-1, 1, self.boundary_size)
        X, Y = np.meshgrid(x, x)
        self.target_boundary = np.exp(1j * 5 * (X**2 + Y**2)).astype(np.complex64)
        self.target_boundary /= np.linalg.norm(self.target_boundary) + 1e-10

        boundary = self.rng.standard_normal((self.boundary_size, self.boundary_size)).astype(np.complex64)
        self.boundary_reality = boundary / (np.linalg.norm(boundary) + 1e-10)

        phase = np.linspace(0, 2 * np.pi, self.bulk_dim)
        psi = np.exp(1j * phase) / np.sqrt(self.bulk_dim)
        self.bulk_rho = np.outer(psi, psi.conj())
        self.history = []

    def holographic_forward(self, rho):
        """Project a bulk density matrix to the boundary representation."""
        upscaled = np.kron(rho, np.ones((self.scale, self.scale), dtype=np.complex64))
        return upscaled / (np.linalg.norm(upscaled) + 1e-10)

    def holographic_backward(self, boundary_grad):
        """Map a boundary gradient back into the bulk matrix space."""
        reshaped = boundary_grad.reshape(
            self.bulk_dim, self.scale, self.bulk_dim, self.scale
        )
        downscaled = np.mean(reshaped, axis=(1, 3))
        return downscaled / (np.linalg.norm(downscaled) + 1e-10)

    def retrocausal_optimization_step(self, learning_rate=0.5):
        """Perform one projected-gradient optimization step."""
        if learning_rate < 0:
            raise ValueError("learning_rate must be non-negative")

        loss_matrix = self.boundary_reality - self.target_boundary
        reality_loss = float(np.real(np.sum(np.abs(loss_matrix) ** 2)))
        grad_boundary = 2.0 * loss_matrix
        grad_rho = self.holographic_backward(grad_boundary)
        grad_rho = (grad_rho + grad_rho.conj().T) / 2.0

        self.bulk_rho = self.bulk_rho - learning_rate * grad_rho
        self.bulk_rho = (self.bulk_rho + self.bulk_rho.conj().T) / 2.0
        eigenvalues, eigenvectors = np.linalg.eigh(self.bulk_rho)
        eigenvalues = np.clip(eigenvalues, 0, None)
        self.bulk_rho = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.conj().T
        self.bulk_rho = self.bulk_rho / (np.trace(self.bulk_rho) + 1e-10)
        self.boundary_reality = self.holographic_forward(self.bulk_rho)

        new_loss = float(np.real(np.sum(np.abs(self.boundary_reality - self.target_boundary) ** 2)))
        eigenvalues = np.clip(np.linalg.eigvalsh(self.bulk_rho), 1e-15, 1.0)
        bulk_entropy = float(np.real(-np.sum(eigenvalues * np.log(eigenvalues))))
        return reality_loss, new_loss, bulk_entropy

    def execute(self, steps=100):
        """Execute optimization steps and return elapsed time plus milestones."""
        if steps < 0:
            raise ValueError("steps must be non-negative")
        start_time = time.perf_counter()
        for step in range(steps):
            loss_before, loss_after, bulk_ent = self.retrocausal_optimization_step()
            if step % 20 == 0 or step == steps - 1:
                self.history.append(
                    {"step": step, "loss_before": loss_before, "loss_after": loss_after,
                     "bulk_entropy": bulk_ent,
                     "optimization_ratio": loss_after / (loss_before + 1e-10)}
                )
        return time.perf_counter() - start_time, self.history
