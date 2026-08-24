from __future__ import annotations

import importlib
import subprocess
import sys

import pytest


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
    assert isinstance(winuvloop.backend_version(), str)


def test_import_is_clean_under_deprecation_warnings_as_errors() -> None:
    subprocess.run(
        [sys.executable, "-W", "error::DeprecationWarning", "-c", "import winuvloop"],
        check=True,
    )


@pytest.mark.parametrize(
    ("version_info", "expected_deprecated_exports"),
    [
        ((3, 15), {"EventLoopPolicy", "install"}),
        ((3, 16), set()),
    ],
)
def test_deprecated_exports_follow_python_lifecycle(
    version_info: tuple[int, int],
    expected_deprecated_exports: set[str],
) -> None:
    code = f"""
import sys
sys.version_info = {version_info!r}
import winuvloop
deprecated_exports = {{"EventLoopPolicy", "install"}}
assert deprecated_exports & set(winuvloop.__all__) == {expected_deprecated_exports!r}
"""
    subprocess.run([sys.executable, "-c", code], check=True)


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
