# Contributing

Thanks for improving `winuvloop`.

## Local Setup

Install `uv`, then run:

```bash
uv sync
```

## Checks

Before opening a pull request, run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build
uv run twine check dist/*
```

Pull requests are gated by the GitHub Actions CI workflow. CI checks the
lockfile, linting, formatting, package build metadata, fake-backend unit tests,
and real-backend smoke tests on Linux, macOS, and Windows.

## Version Policy

`winuvloop` follows semantic versioning:

- Patch releases fix packaging, documentation, tests, or compatible behavior.
- Minor releases add public API or support for new Python/backend versions.
- Major releases remove compatibility or change public behavior.

Releases are automatic after a version change lands on `main`. If
`pyproject.toml` contains a version without a matching `vX.Y.Z` tag, GitHub
Actions creates the tag after CI has passed for `main` and dispatches
`release.yml`. The release workflow builds, validates, publishes to PyPI
through trusted publishing or the `PYPI_API_TOKEN` fallback secret, and creates
a GitHub Release.

## Dependency Policy

Runtime dependencies should stay aligned with supported `uvloop` and `winloop`
releases. Avoid upper bounds unless a known incompatibility exists; upper bounds
can block users from receiving fixed wheels and security releases.

Development dependencies are locked with `uv.lock` and updated by Dependabot.
Dependabot pull requests are merged automatically after CI passes.

Dependency updates should preserve the package's compatibility promise:

- keep runtime dependencies aligned with the latest usable `uvloop` and
  `winloop` releases
- keep CI covering at least one oldest-supported CPython, one current CPython,
  one pre-release/new CPython when available, and all three runner families
- prefer improving diagnostics over adding fallback event-loop behavior that
  differs from upstream

## Pull Request Guidelines

- Keep changes focused.
- Add tests for runtime behavior.
- Update `README.md` or `CHANGELOG.md` when user-facing behavior changes.
- Do not vendor code from `uvloop` or `winloop`; this package should remain a
  thin selector and compatibility wrapper.
- When reporting backend bugs, first try to reproduce with `uvloop` or
  `winloop` imported directly so the issue can be routed to the right project.
