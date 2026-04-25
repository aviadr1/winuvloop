from __future__ import annotations

import importlib
import sys


def import_real_winuvloop():
    sys.modules.pop("winuvloop", None)
    return importlib.import_module("winuvloop")


async def answer() -> int:
    return 42


def test_real_backend_matches_platform() -> None:
    winuvloop = import_real_winuvloop()
    expected = "winloop" if sys.platform == "win32" else "uvloop"

    assert winuvloop.backend_name() == expected
    assert winuvloop.__backend__ == expected
    assert winuvloop.backend().__name__ == expected


def test_real_backend_runs_coroutine() -> None:
    winuvloop = import_real_winuvloop()

    assert winuvloop.run(answer()) == 42


def test_real_backend_exposes_loop_factory() -> None:
    winuvloop = import_real_winuvloop()
    loop = winuvloop.new_event_loop()
    try:
        assert isinstance(loop, winuvloop.Loop)
    finally:
        loop.close()
