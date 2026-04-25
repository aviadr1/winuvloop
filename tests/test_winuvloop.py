from __future__ import annotations

import importlib
import sys
import types

import pytest


class FakeLoop:
    pass


class FakePolicy:
    pass


def fake_backend(name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__version__ = f"{name}-version"
    module.run = lambda main, **kwargs: ("run", name, main, kwargs)
    module.install = lambda: ("install", name)
    module.new_event_loop = lambda: FakeLoop()
    module.Loop = FakeLoop
    module.EventLoopPolicy = FakePolicy
    module.backend_only = "delegated"
    return module


def import_winuvloop(monkeypatch: pytest.MonkeyPatch, platform: str):
    monkeypatch.setattr(sys, "platform", platform)
    monkeypatch.setitem(sys.modules, "uvloop", fake_backend("uvloop"))
    monkeypatch.setitem(sys.modules, "winloop", fake_backend("winloop"))
    sys.modules.pop("winuvloop", None)
    return importlib.import_module("winuvloop")


@pytest.mark.parametrize(
    ("platform", "expected"),
    [
        ("win32", "winloop"),
        ("linux", "uvloop"),
        ("darwin", "uvloop"),
        ("cygwin", "uvloop"),
    ],
)
def test_selects_backend_from_platform(
    monkeypatch: pytest.MonkeyPatch, platform: str, expected: str
) -> None:
    winuvloop = import_winuvloop(monkeypatch, platform)

    assert winuvloop.backend_name() == expected
    assert winuvloop.__backend__ == expected
    assert winuvloop.backend().__name__ == expected


def test_reexports_backend_api(monkeypatch: pytest.MonkeyPatch) -> None:
    winuvloop = import_winuvloop(monkeypatch, "linux")

    assert winuvloop.run("main") == ("run", "uvloop", "main", {})
    assert winuvloop.install() == ("install", "uvloop")
    assert isinstance(winuvloop.new_event_loop(), FakeLoop)
    assert winuvloop.Loop is FakeLoop
    assert winuvloop.EventLoopPolicy is FakePolicy


def test_delegates_backend_specific_attributes(monkeypatch: pytest.MonkeyPatch) -> None:
    winuvloop = import_winuvloop(monkeypatch, "win32")

    assert winuvloop.backend_only == "delegated"


def test_exposes_backend_version_for_support_logs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    winuvloop = import_winuvloop(monkeypatch, "linux")

    def missing_distribution(name: str) -> str:
        raise winuvloop.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(winuvloop.metadata, "version", missing_distribution)

    assert winuvloop.backend_version() == "uvloop-version"


def test_missing_attributes_raise_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    winuvloop = import_winuvloop(monkeypatch, "linux")

    missing = "not_a_real_attribute"
    with pytest.raises(AttributeError, match="winuvloop"):
        getattr(winuvloop, missing)


def test_missing_backend_error_names_selected_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_import_module = importlib.import_module

    def import_module(name: str, package: str | None = None):
        if name == "uvloop":
            raise ModuleNotFoundError("No module named 'uvloop'", name=name)
        return real_import_module(name, package)

    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(importlib, "import_module", import_module)
    monkeypatch.delitem(sys.modules, "winuvloop", raising=False)

    with pytest.raises(ModuleNotFoundError, match="uvloop.*CPython"):
        real_import_module("winuvloop")


def test_nested_backend_import_errors_are_preserved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_import_module = importlib.import_module

    def import_module(name: str, package: str | None = None):
        if name == "uvloop":
            raise ModuleNotFoundError("No module named 'uvloop_dependency'", name="x")
        return real_import_module(name, package)

    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(importlib, "import_module", import_module)
    monkeypatch.delitem(sys.modules, "winuvloop", raising=False)

    with pytest.raises(ModuleNotFoundError, match="uvloop_dependency"):
        real_import_module("winuvloop")


def test_all_exports_are_names(monkeypatch: pytest.MonkeyPatch) -> None:
    winuvloop = import_winuvloop(monkeypatch, "linux")

    assert all(isinstance(name, str) for name in winuvloop.__all__)
    expected = {"run", "install", "new_event_loop", "backend_name", "backend_version"}
    assert expected <= set(winuvloop.__all__)
