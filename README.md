# winuvloop

[![PyPI](https://img.shields.io/pypi/v/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![Python](https://img.shields.io/pypi/pyversions/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![Downloads](https://img.shields.io/pypi/dm/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![CI](https://github.com/aviadr1/winuvloop/actions/workflows/ci.yml/badge.svg)](https://github.com/aviadr1/winuvloop/actions/workflows/ci.yml)
[![License](https://img.shields.io/pypi/l/winuvloop.svg)](https://github.com/aviadr1/winuvloop/blob/main/LICENSE)

`winuvloop` is a tiny cross-platform asyncio event loop selector:

| Platform | Backend used by `winuvloop` |
| --- | --- |
| Windows | [`winloop`](https://github.com/Vizonex/Winloop) |
| Linux, macOS, POSIX | [`uvloop`](https://github.com/MagicStack/uvloop) |

It is useful when the same Python application, example, benchmark, CLI, or
service should use a high-performance asyncio loop on both Windows and
Unix-like systems without duplicating platform checks at every entry point.

## Why This Exists

[`uvloop`](https://github.com/MagicStack/uvloop) is the established
high-performance asyncio event loop for Linux, macOS, and other POSIX
platforms. It is widely used for network-heavy asyncio workloads such as API
servers, proxies, websocket services, crawlers, and async database clients.

[`winloop`](https://github.com/Vizonex/Winloop) provides a uvloop-compatible
API for Windows, where `uvloop` itself is not the Windows backend.

`winuvloop` does not replace either upstream project. It gives you one import
that chooses the right upstream backend:

```python
import winuvloop


async def main() -> None:
    ...


winuvloop.run(main())
```

## When To Use It

Use `winuvloop` when:

- your project supports both Windows and Linux/macOS
- examples or docs should stay platform-neutral
- your CLI or application wants the fastest available asyncio loop by default
- you want one dependency that resolves `uvloop` or `winloop` through platform
  markers
- you want to log or inspect which optimized backend was selected

Use the upstream packages directly when:

- your project only targets Linux/macOS: use `uvloop`
- your project only targets Windows: use `winloop`
- you need backend-specific APIs and do not want a selector layer
- you are debugging an upstream event-loop issue and need to remove wrappers

## Installation

```bash
pip install winuvloop
```

With `uv`:

```bash
uv add winuvloop
```

`winuvloop` declares platform-specific dependencies. Installers resolve only
the backend needed for the current environment.

## Usage

Prefer `run()` for application entry points:

```python
import winuvloop


async def main() -> str:
    return "done"


result = winuvloop.run(main())
```

For frameworks or legacy code that expects a global event-loop policy, use
`install()`:

```python
import asyncio

import winuvloop


winuvloop.install()
asyncio.run(main())
```

You can inspect the selected backend for diagnostics and support logs:

```python
import winuvloop


print(winuvloop.backend_name())  # "uvloop" or "winloop"
print(winuvloop.__backend__)
print(winuvloop.backend().__name__)
```

The module re-exports the common backend API:

- `run`
- `install`
- `new_event_loop`
- `Loop`
- `EventLoopPolicy`

Backend-specific attributes are delegated to the selected upstream module.

## Typing

`winuvloop` ships a `py.typed` marker and public API stubs for the selector
module. The runtime values remain direct aliases to the selected upstream
backend, so `winuvloop.Loop` is still `uvloop.Loop` on POSIX and `winloop.Loop`
on Windows.

## Compatibility

`winuvloop` targets CPython 3.8.1 and newer, matching the current published
support range of `uvloop` and `winloop`.

| Environment | Status |
| --- | --- |
| CPython 3.8-3.14 | Supported by current upstream wheels |
| Linux/macOS | Uses `uvloop` |
| Windows | Uses `winloop` |
| PyPy | Not supported by the upstream native backends |
| Windows ARM64 | Supported when `winloop` publishes a matching wheel |
| Linux/macOS ARM64 | Supported when `uvloop` publishes a matching wheel |

If an upstream backend does not publish a wheel for a specific interpreter or
platform, installation may require local build tooling for that backend.

## Testing Strategy

CI runs on Linux, macOS, and Windows. It includes:

- lockfile validation with `uv lock --check`
- linting with `ruff`
- wrapper unit tests that mock both backends
- real backend smoke tests that call `winuvloop.run()` on the platform backend
- source distribution and wheel builds
- package metadata validation with `twine check`

This keeps the wrapper behavior fast to test while still proving that the
published backend dependencies are usable on each runner family.

## Development

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management,
locking, and builds.

```bash
uv sync
uv run ruff check .
uv run pytest
uv build
uv run twine check dist/*
```

## Release And Automation

Dependabot updates are grouped for upstream event loops, Python tooling, and
GitHub Actions. Dependabot PRs auto-merge after the CI workflow passes.

Releases are automatic:

1. Change `project.version` in `pyproject.toml`.
2. Merge to `main`.
3. GitHub Actions creates the missing `vX.Y.Z` tag.
4. GitHub Actions dispatches `release.yml` for that tag.
5. The release workflow builds, validates, publishes to PyPI, and creates a
   GitHub Release.

PyPI trusted publishing must be configured for the `release.yml` workflow and
the `pypi` environment for credential-free publishing. If the repository still
uses a `PYPI_API_TOKEN` secret, the release workflow can use that as a fallback.
Manual tag pushes with the `vX.Y.Z` format still run the same release workflow.

## License

MIT. See [LICENSE](LICENSE).
