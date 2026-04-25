# Changelog

All notable changes to `winuvloop` are documented here.

## 0.2.2 - Unreleased

- Add public API stubs for better editor and type-checker ergonomics.

## 0.2.1 - 2026-04-25

- Move packaging to standard PEP 621 metadata and the `uv_build` backend.
- Replace `poetry.lock` with `uv.lock` for faster, reproducible development.
- Add PyPI project URLs for GitHub, issues, changelog, `uvloop`, and `winloop`.
- Use a modern `src/` package layout.
- Re-export `new_event_loop`, `Loop`, and `EventLoopPolicy` in addition to
  `run` and `install`.
- Add `backend_name()`, `backend()`, and `__backend__` for support visibility.
- Add a typed package marker.
- Add pytest coverage for platform selection, exports, and backend delegation.
- Add real backend smoke tests for CI compatibility coverage.
- Add ruff linting.
- Replace the release workflow with a tag-based trusted publishing flow.
- Add automatic release tagging from `pyproject.toml` versions on `main`.
- Add GitHub Release creation with release artifacts.
- Add a CI workflow for lockfile checks, linting, tests, build validation, and
  package metadata checks.
- Add Dependabot auto-merge after CI passes.
- Update Dependabot to track `uv` dependencies and GitHub Actions.

## 0.2.0

- Use latest platform backend packages through unconstrained Poetry
  dependencies.

## 0.1.0

- Initial wrapper around `uvloop` on POSIX and `winloop` on Windows.
