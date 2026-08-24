"""Phase 7: holographic bulk-to-boundary projection diagnostics."""

import time

import numpy as np


class HolographicProjectionEngine:
    """Project a normalized complex bulk state onto a larger boundary matrix."""

    def __init__(self, bulk_dim=32, boundary_size=64, seed=None):
        if bulk_dim < 1 or boundary_size < 1:
            raise ValueError("bulk_dim and boundary_size must be positive")
        if boundary_size % bulk_dim != 0:
            raise ValueError("boundary_size must be divisible by bulk_dim")
        self.bulk_dim = int(bulk_dim)
        self.boundary_size = int(boundary_size)
        self.scale = self.boundary_size // self.bulk_dim
        self.rng = np.random.default_rng(seed)

        phase = np.linspace(0, 2 * np.pi, self.bulk_dim)
        self.bulk_state = np.exp(1j * phase) / np.sqrt(self.bulk_dim)
        boundary = self.rng.standard_normal((self.boundary_size, self.boundary_size)).astype(np.complex64) * 1e-6
        self.boundary_reality = boundary / (np.linalg.norm(boundary) + 1e-10)
        self.history = []

    @staticmethod
    def compute_holographic_entropy(matrix):
        """Return von Neumann entropy of the normalized Gram density matrix."""
        rho = matrix @ matrix.conj().T
        rho = rho / np.trace(rho)
        eigenvalues = np.clip(np.linalg.eigvalsh(rho), 1e-15, 1.0)
        return float(np.real(-np.sum(eigenvalues * np.log(eigenvalues))))

    @staticmethod
    def compute_emergent_fractal_dimension(matrix):
        """Estimate a spectral/fractal dimension from radial Fourier scaling."""
        fft_matrix = np.fft.fft2(np.abs(matrix))
        power_spectrum = np.fft.fftshift(np.abs(fft_matrix) ** 2)
        y, x = np.indices(power_spectrum.shape)
        center_x = power_spectrum.shape[1] // 2
        center_y = power_spectrum.shape[0] // 2
        radius = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2).astype(int)
        tbin = np.bincount(radius.ravel(), power_spectrum.ravel())
        nr = np.bincount(radius.ravel())
        radial_profile = tbin / np.where(nr > 0, nr, 1)
        half_len = len(radial_profile) // 2
        k = np.arange(1, half_len)
        coeffs = np.polyfit(np.log(k), np.log(radial_profile[1:half_len] + 1e-10), 1)
        beta = -coeffs[0]
        return float(np.clip((beta + 2) / 2.0, 1.0, 3.0))

    def holographic_projection_step(self):
        """Perform one bulk-to-boundary coupling step."""
        bulk_projector = np.outer(self.bulk_state, self.bulk_state.conj())
        upscaled_projector = np.kron(
            bulk_projector,
            np.ones((self.scale, self.scale), dtype=np.complex64),
        )
        coupling_strength = 0.15
        self.boundary_reality = (
            (1.0 - coupling_strength) * self.boundary_reality
            + coupling_strength * upscaled_projector * np.exp(1j * np.angle(self.boundary_reality))
        )
        norm = np.linalg.norm(self.boundary_reality)
        if norm > 1e-6:
            self.boundary_reality = self.boundary_reality / norm * np.sqrt(self.boundary_size)

        bulk_coherence = float(np.abs(np.sum(self.bulk_state)) ** 2)
        boundary_entropy = self.compute_holographic_entropy(self.boundary_reality)
        fractal_dim = self.compute_emergent_fractal_dimension(self.boundary_reality)
        return bulk_coherence, boundary_entropy, fractal_dim

    def execute(self, steps=100):
        """Execute projection steps and return elapsed time plus milestones."""
        if steps < 0:
            raise ValueError("steps must be non-negative")
        start_time = time.perf_counter()
        for step in range(steps):
            bulk_coh, bound_ent, frac_dim = self.holographic_projection_step()
            if step % 20 == 0 or step == steps - 1:
                self.history.append(
                    {"step": step, "bulk_coherence": bulk_coh,
                     "boundary_entropy": bound_ent, "fractal_dimension": frac_dim}
                )
        return time.perf_counter() - start_time, self.history
