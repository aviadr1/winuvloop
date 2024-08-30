import asyncio as __asyncio
import sys
import typing as _typing
from asyncio.events import BaseDefaultEventLoopPolicy as __BasePolicy

_T = _typing.TypeVar("_T")


if not _typing.TYPE_CHECKING:

    if sys.platform in ("win32", "cygwin", "cli"):
        import winloop

        EventLoopPolicy = winloop.EventLoopPolicy
        new_event_loop = winloop.new_event_loop
        Loop = winloop.Loop
        run = winloop.run
        install = winloop.install
    else:
        import uvloop

        EventLoopPolicy = uvloop.EventLoopPolicy
        new_event_loop = uvloop.new_event_loop
        Loop = uvloop.Loop
        run = uvloop.run
        install = uvloop.install

else:

    class Loop(__asyncio.BaseEventLoop):  # type: ignore
        pass

    def new_event_loop() -> Loop:
        """Return a new event loop."""
        ...

    def install() -> None:
        """A helper function to install uvloop/winloop policy."""

    def run(
        main: _typing.Coroutine[_typing.Any, _typing.Any, _T],
        *,
        loop_factory: _typing.Optional[_typing.Callable[[], Loop]] = new_event_loop,
        debug: _typing.Optional[bool] = None,
    ) -> _T:
        """The preferred way of running a coroutine with winuvloop."""

    class EventLoopPolicy(__BasePolicy):
        """Event loop policy.

        The preferred way to make your application use winuvloop:

        >>> import asyncio
        >>> import winuvloop
        >>> asyncio.set_event_loop_policy(winuvloop.EventLoopPolicy())
        >>> asyncio.get_event_loop()

        """

        def _loop_factory(self) -> Loop:...

        if _typing.TYPE_CHECKING:
            # EventLoopPolicy doesn't implement these, but since they are marked
            # as abstract in typeshed, we have to put them in so mypy thinks
            # the base methods are overridden. This is the same approach taken
            # for the Windows event loop policy classes in typeshed.
            def get_child_watcher(self) -> _typing.NoReturn: ...

            def set_child_watcher(self, watcher: _typing.Any) -> _typing.NoReturn: ...


__all__ = ["run", "install", "EventLoopPolicy", "Loop", "new_event_loop"]

