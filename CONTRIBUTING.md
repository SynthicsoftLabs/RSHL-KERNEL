# Contributing to RSHL-KERNEL

Thank you for contributing to RSHL-KERNEL.

## Development principles

- Preserve the nine-phase architecture and public engine names unless a compatibility change is explicitly intended.
- Do not remove an existing mathematical or diagnostic capability when adding a new implementation.
- Distinguish exact algebraic identities from numerical approximations and research hypotheses.
- Prefer deterministic random-number generators (`numpy.random.default_rng`) for new code.
- Add tests for every new invariant, identity, edge case, or public API behavior.
- Keep public methods documented and maintain readable numerical code.
- Avoid unnecessary dense O(n^3) operations when a low-rank formulation is available.

## Local setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# POSIX: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Verification

Run the complete suite:

```bash
pytest -v
```

Format code with Black:

```bash
black rshl_kernel tests
```

Run static checking:

```bash
mypy rshl_kernel/ --ignore-missing-imports
```

## Mathematical changes

When changing an equation or numerical method, document:

1. the original formulation;
2. the new formulation;
3. why the change is required;
4. the expected numerical consequences;
5. tests demonstrating the intended behavior.

For identity implementations, retain a dense reference test at a manageable dimension whenever practical.

## Pull requests

Pull requests should explain the engineering and mathematical impact of the change. Avoid describing a numerical proxy as a proven physical result. Include test evidence and note any intentional API or output-schema changes.
