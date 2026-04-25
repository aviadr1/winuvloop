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
uv run pytest
uv build
uv run twine check dist/*
```

## Version Policy

`winuvloop` follows semantic versioning:

- Patch releases fix packaging, documentation, tests, or compatible behavior.
- Minor releases add public API or support for new Python/backend versions.
- Major releases remove compatibility or change public behavior.

Releases are automatic after a version change lands on `main`. If
`pyproject.toml` contains a version without a matching `vX.Y.Z` tag, GitHub
Actions creates the tag and dispatches `release.yml`. The release workflow
builds, validates, publishes to PyPI through trusted publishing or the
`PYPI_API_TOKEN` fallback secret, and creates a GitHub Release.

## Dependency Policy

Runtime dependencies should stay aligned with supported `uvloop` and `winloop`
releases. Avoid upper bounds unless a known incompatibility exists; upper bounds
can block users from receiving fixed wheels and security releases.

Development dependencies are locked with `uv.lock` and updated by Dependabot.
Dependabot pull requests are merged automatically after CI passes.

## Pull Request Guidelines

- Keep changes focused.
- Add tests for runtime behavior.
- Update `README.md` or `CHANGELOG.md` when user-facing behavior changes.
- Do not vendor code from `uvloop` or `winloop`; this package should remain a
  thin selector and compatibility wrapper.
