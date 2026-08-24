# Changelog

All notable changes to RSHL-KERNEL are documented here.

## [Unreleased]

### Engineering and documentation

- Professionalized package metadata and project URLs.
- Declared BSD-2-Clause consistently in package metadata and documentation.
- Added Python tooling configuration for pytest, Black, and mypy.
- Added repository-wide Python ignore rules.
- Added comprehensive mathematical foundations documentation covering all nine phases.
- Added contribution and research-quality engineering guidance.
- Expanded automated test coverage across all nine public engines.
- Strengthened deterministic mathematical identity tests.
- Professionalized phase implementations with module documentation, validation, deterministic RNG handling, and clearer numerical diagnostics.
- Clarified where topology, curvature, holographic, retrocausal, and convergence quantities are numerical proxies rather than claims beyond the implemented model.

### Compatibility

The existing nine public engine classes remain exported from `rshl_kernel`:

- `SingularityEngine`
- `WoodburyEngine`
- `AdaptiveWoodburyEngine`
- `RicciFlowWoodburyEngine`
- `TopologicalRicciFlowEngine`
- `QuantumTopologicalEngine`
- `HolographicProjectionEngine`
- `RetrocausalHolographicEngine`
- `IdentityConvergenceEngine`

