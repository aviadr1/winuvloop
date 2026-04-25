"""Choose the fastest available asyncio event loop for the current platform."""

from __future__ import annotations

import sys
from importlib import import_module, metadata
from platform import python_implementation
from types import ModuleType
from typing import Any


def backend_name() -> str:
    """Return the event-loop package selected for this interpreter."""
    return "winloop" if sys.platform == "win32" else "uvloop"


def backend() -> ModuleType:
    """Return the imported event-loop backend module."""
    return _BACKEND


def backend_version() -> str | None:
    """Return the installed version of the selected backend, if known."""
    try:
        return metadata.version(_BACKEND_NAME)
    except metadata.PackageNotFoundError:
        version = getattr(_BACKEND, "__version__", None)
        return version if isinstance(version, str) else None


_BACKEND_NAME = backend_name()

try:
    _BACKEND = import_module(_BACKEND_NAME)
except ModuleNotFoundError as exc:
    if exc.name != _BACKEND_NAME:
        raise
    raise ModuleNotFoundError(
        f"winuvloop selected {_BACKEND_NAME!r} for platform {sys.platform!r}, "
        f"but that package is not installed for {python_implementation()}. "
        f"winuvloop's optimized backends target CPython. Install winuvloop "
        f"with its platform dependencies, or install {_BACKEND_NAME!r} "
        f"directly."
    ) from exc

__backend__ = _BACKEND.__name__

try:
    __version__ = metadata.version("winuvloop")
except metadata.PackageNotFoundError:  # pragma: no cover - editable tree fallback
    __version__ = "0.0.0"

run = _BACKEND.run
install = _BACKEND.install
new_event_loop = _BACKEND.new_event_loop
Loop = _BACKEND.Loop
EventLoopPolicy = _BACKEND.EventLoopPolicy

__all__ = (
    "EventLoopPolicy",
    "Loop",
    "__backend__",
    "__version__",
    "backend",
    "backend_name",
    "backend_version",
    "install",
    "new_event_loop",
    "run",
)


def __getattr__(name: str) -> Any:
    """Delegate backend-specific attributes that are not wrapped explicitly."""
    try:
        return getattr(_BACKEND, name)
    except AttributeError as exc:
        raise AttributeError(f"module 'winuvloop' has no attribute {name!r}") from exc
