# winuvloop

[![PyPI](https://img.shields.io/pypi/v/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![Python](https://img.shields.io/pypi/pyversions/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![CI](https://github.com/aviadr1/winuvloop/actions/workflows/ci.yml/badge.svg)](https://github.com/aviadr1/winuvloop/actions/workflows/ci.yml)
[![License](https://img.shields.io/pypi/l/winuvloop.svg)](https://github.com/aviadr1/winuvloop/blob/main/LICENSE)

`winuvloop` is a small cross-platform asyncio helper that selects the fastest
event loop for the operating system:

| Platform | Backend |
| --- | --- |
| Windows | [`winloop`](https://github.com/Vizonex/Winloop) |
| Linux, macOS, POSIX | [`uvloop`](https://github.com/MagicStack/uvloop) |

Use it when an application, library example, benchmark, or internal service
should run with `uvloop` on Unix-like systems and `winloop` on Windows without
duplicating platform checks in every entry point.

## Why

`uvloop` is the common high-performance event loop for asyncio applications on
Linux and macOS. `winloop` brings a compatible API to Windows. `winuvloop`
keeps the import and setup code the same across platforms:

```python
import winuvloop


async def main() -> None:
    ...


winuvloop.run(main())
```

## Installation

```bash
pip install winuvloop
```

With `uv`:

```bash
uv add winuvloop
```

`winuvloop` declares platform-specific dependencies, so installers only resolve
the backend needed for the current environment.

## Usage

Prefer `run()` for new application entry points:

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

You can also inspect which backend was selected:

```python
import winuvloop


print(winuvloop.backend_name())  # "uvloop" or "winloop"
print(winuvloop.__backend__)
```

The module re-exports the common backend API:

- `run`
- `install`
- `new_event_loop`
- `Loop`
- `EventLoopPolicy`

Backend-specific attributes are delegated to the selected upstream module.

## Compatibility

`winuvloop` targets CPython 3.8.1 and newer, matching the current published
support range of `uvloop` and `winloop`.

| Python | Status |
| --- | --- |
| 3.8-3.14 | Supported by current upstream wheels |
| PyPy | Not supported by `uvloop` or `winloop` |
| Windows ARM64 | Supported when `winloop` publishes a matching wheel |
| Linux/macOS ARM64 | Supported when `uvloop` publishes a matching wheel |

If an upstream backend does not publish a wheel for a specific interpreter or
platform, installation may require local build tooling for that backend.

## Development

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management,
locking, and builds.

```bash
uv sync
uv run pytest
uv run ruff check .
uv build
uv run twine check dist/*
```

The test suite mocks `uvloop` and `winloop` so wrapper behavior can be validated
quickly without compiling native extensions on every platform.

## Release

Releases are built by GitHub Actions from `v*.*.*` tags and published to PyPI
using trusted publishing. The PyPI project metadata links back to GitHub,
issues, changelog, and the upstream backend projects for better discoverability.

## License

MIT. See [LICENSE](LICENSE).
