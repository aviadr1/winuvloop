# winuvloop

[![PyPI](https://img.shields.io/pypi/v/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![Python](https://img.shields.io/pypi/pyversions/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![Downloads](https://img.shields.io/pypi/dm/winuvloop.svg)](https://pypi.org/project/winuvloop/)
[![CI](https://github.com/aviadr1/winuvloop/actions/workflows/ci.yml/badge.svg)](https://github.com/aviadr1/winuvloop/actions/workflows/ci.yml)
[![License](https://img.shields.io/pypi/l/winuvloop.svg)](https://github.com/aviadr1/winuvloop/blob/main/LICENSE)

`winuvloop` is a tiny cross-platform asyncio event loop selector for projects
that want one import to do the right thing on developer laptops, CI, and
production runners:

| Platform | Backend used by `winuvloop` |
| --- | --- |
| Windows | [`winloop`](https://github.com/Vizonex/Winloop) |
| Linux, macOS, other POSIX | [`uvloop`](https://github.com/MagicStack/uvloop) |

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

`winuvloop` does not replace either upstream project, vendor their code, or
hide backend bugs. It gives you one import that chooses the right upstream
backend:

```python
import winuvloop


async def main() -> None:
    ...


winuvloop.run(main())
```

The wrapper stays deliberately small: platform detection, clear diagnostics,
common API re-exports, typing stubs, and platform-specific dependency markers.
Runtime behavior comes from the selected upstream backend.

## Why Performance Can Matter

The upstream projects publish benchmark guidance for the workloads they own.
[`uvloop`](https://github.com/MagicStack/uvloop#performance) reports making
asyncio 2-4x faster on its echo-server benchmarks. On Windows,
[`winloop`](https://github.com/Vizonex/Winloop#benchmarks) reports a TCP
connection benchmark of 0.493s with `WinLoopPolicy`, compared with 2.510s for
`WindowsProactorEventLoopPolicy` and 2.723s for
`WindowsSelectorEventLoopPolicy`.

Those are upstream benchmark numbers, not a universal promise for every
application. The practical point for `winuvloop` is simpler: one dependency
lets a cross-platform project select the optimized backend that upstream
projects already benchmark and maintain for each operating system family.

## When To Use It

Use `winuvloop` when:

- your project supports both Windows and Linux/macOS
- examples or docs should stay platform-neutral
- your CLI or application wants the fastest available asyncio loop by default
- you want one dependency that resolves `uvloop` or `winloop` through platform
  markers
- you want to log or inspect which optimized backend was selected
- you maintain library examples that should work for both Unix and Windows
  users

Use the upstream packages directly when:

- your project only targets Linux/macOS: use `uvloop`
- your project only targets Windows: use `winloop`
- you need backend-specific APIs and do not want a selector layer
- you are debugging an upstream event-loop issue and need to remove wrappers

| Situation | Recommended dependency |
| --- | --- |
| Linux/macOS-only service | `uvloop` |
| Windows-only service | `winloop` |
| Cross-platform CLI, app, benchmark, or documentation | `winuvloop` |
| Backend-specific feature work or bug isolation | upstream backend directly |

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
print(winuvloop.backend_version())
print(winuvloop.__backend__)
print(winuvloop.backend().__name__)
```

The module re-exports the common backend API:

- `run`
- `install`
- `new_event_loop`
- `Loop`
- `EventLoopPolicy`
- `backend`
- `backend_name`
- `backend_version`

Backend-specific attributes are delegated to the selected upstream module.

## Framework Examples

`winuvloop` is most useful at process entry points: command-line scripts,
application launchers, benchmark runners, and local development helpers. Install
the optimized loop before a framework creates its event loop, or use
`winuvloop.run()` when you own the top-level coroutine.

These examples do not mean `winuvloop` depends on the frameworks shown here.
Install FastAPI, Uvicorn, aiohttp, or any other framework separately in your
application.

### FastAPI And Uvicorn

For a FastAPI application launched from Python, install the selected backend
before calling `uvicorn.run()`. Pass `loop="asyncio"` so Uvicorn uses the event
loop policy that `winuvloop.install()` already selected:

```python
# serve.py
import uvicorn

import winuvloop


winuvloop.install()

uvicorn.run(
    "myapp:app",
    host="127.0.0.1",
    port=8000,
    loop="asyncio",
)
```

Then run the launcher instead of invoking `uvicorn` directly:

```bash
python serve.py
```

If your deployment platform already configures the event loop, prefer the
platform's documented setting. `winuvloop` is the portable option when you want
the same launcher to select `uvloop` on Linux/macOS and `winloop` on Windows.

### aiohttp Web Server

For an `aiohttp.web` application, use `winuvloop.run()` around the application
runner:

```python
import asyncio

from aiohttp import web

import winuvloop


async def hello(request: web.Request) -> web.Response:
    return web.Response(text="hello")


async def main() -> None:
    app = web.Application()
    app.router.add_get("/", hello)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "127.0.0.1", 8080)
    await site.start()

    await asyncio.Event().wait()


winuvloop.run(main())
```

### Async CLI Or Worker

For scripts, CLIs, and workers, keep the entry point boring:

```python
import winuvloop


async def main() -> int:
    ...
    return 0


raise SystemExit(winuvloop.run(main()))
```

This keeps examples and internal tools platform-neutral while still selecting
the optimized backend for the current runner.

### Tests And Support Logs

For compatibility tests, assert the selected backend rather than hard-coding an
operating system in every test:

```python
import sys

import winuvloop


def test_optimized_backend_is_available() -> None:
    expected = "winloop" if sys.platform == "win32" else "uvloop"

    assert winuvloop.backend_name() == expected
    assert winuvloop.backend_version() is not None
```

For issue reports, include this diagnostic snippet:

```bash
python - <<'PY'
import platform
import winuvloop

print("python:", platform.python_version(), platform.python_implementation())
print("platform:", platform.platform())
print("backend:", winuvloop.backend_name(), winuvloop.backend_version())
PY
```

## Typing

`winuvloop` ships a `py.typed` marker and public API stubs for the selector
module. The runtime values remain direct aliases to the selected upstream
backend, so `winuvloop.Loop` is still `uvloop.Loop` on POSIX and `winloop.Loop`
on Windows.

## Compatibility

`winuvloop` targets CPython 3.8.1 and newer. The optimized backend packages are
native CPython packages, so PyPy and other Python implementations are not a
supported target for this selector.

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

## Upstream Support Boundary

Report selector problems here when platform selection, dependency markers,
typing stubs, documentation, or packaging are wrong.

Report backend behavior problems upstream when the issue also reproduces after
importing the selected backend directly:

- `uvloop`: <https://github.com/MagicStack/uvloop/issues>
- `winloop`: <https://github.com/Vizonex/Winloop/issues>

This keeps backend fixes close to the projects that own event-loop internals
while keeping `winuvloop` focused on cross-platform ergonomics.

## Testing Strategy

CI runs on Linux, macOS, and Windows. It includes:

- lockfile validation with `uv lock --check`
- linting with `ruff`
- formatting checks with `ruff format --check`
- bytecode compilation checks for `src` and `tests`
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
uv run ruff format --check .
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
3. After CI passes on `main`, GitHub Actions creates the missing `vX.Y.Z` tag.
4. GitHub Actions dispatches `release.yml` for that tag.
5. The release workflow smoke-tests Linux, macOS, and Windows, then builds,
   validates, publishes to PyPI, and creates a GitHub Release.

PyPI trusted publishing must be configured for the `release.yml` workflow and
the `pypi` environment for credential-free publishing. If the repository still
uses a `PYPI_API_TOKEN` secret, the release workflow can use that as a fallback.
Manual tag pushes with the `vX.Y.Z` format still run the same release workflow.

## License

MIT. See [LICENSE](LICENSE).
