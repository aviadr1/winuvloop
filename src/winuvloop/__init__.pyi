from __future__ import annotations

import asyncio
import sys
from types import ModuleType
from typing import Any, Callable, Coroutine, TypeVar

_T = TypeVar("_T")

__backend__: str
__version__: str

class Loop(asyncio.AbstractEventLoop): ...

def backend_name() -> str: ...
def backend() -> ModuleType: ...
def backend_version() -> str | None: ...
def new_event_loop() -> Loop: ...
def run(
    main: Coroutine[Any, Any, _T],
    *,
    loop_factory: Callable[[], Loop] | None = ...,
    debug: bool | None = ...,
    **run_kwargs: Any,
) -> _T: ...

if sys.version_info < (3, 16):
    class EventLoopPolicy(asyncio.AbstractEventLoopPolicy): ...

    def install() -> None: ...

def __getattr__(name: str) -> Any: ...
