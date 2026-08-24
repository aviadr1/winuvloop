# Changelog

All notable changes to `winuvloop` are documented here.

## Unreleased

- Avoid loading deprecated event-loop policy compatibility APIs during import
  on Python 3.14.

## 0.2.4 - 2026-04-25

- Add FastAPI/Uvicorn, aiohttp, async CLI, and compatibility-test examples to
  the README.
- Add upstream uvloop and winloop benchmark references to the README.
- Add framework and protocol keywords to improve PyPI discoverability.

## 0.2.3 - 2026-04-25

- Add `backend_version()` for support logs and diagnostics.
- Improve missing-backend import errors with Python implementation context.
- Expand README guidance for `uvloop`, `winloop`, and `winuvloop` selection.
- Gate automatic release tagging on successful `main` CI runs.
- Add release smoke tests on Linux, macOS, and Windows before publishing.
- Add formatting and bytecode compilation checks to CI.
- Add upstream issue routing links and stronger pull request guidance.
- Include tests and maintenance docs in the source distribution.
- Keep Python 3.9 development installs on the compatible Twine line so
  Dependabot security updates can resolve.

## 0.2.2 - 2026-04-25

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
