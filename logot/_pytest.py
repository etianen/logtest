from __future__ import annotations

from collections.abc import Generator
from pkgutil import resolve_name
from typing import Any, Callable

import pytest

from logot._logot import Logot
from logot._typing import T
from logot._wait import AsyncWaiter

MISSING: Any = object()


def pytest_addoption(parser: pytest.Parser, pluginmanager: pytest.PytestPluginManager) -> None:
    group = parser.getgroup("logot")
    _add_option(
        parser,
        group,
        name="level",
        help="The `level` used for automatic `logot` log capturing",
    )
    _add_option(
        parser,
        group,
        name="logger",
        help="The `logger` used for automatic `logot` log capturing",
    )
    _add_option(
        parser,
        group,
        name="timeout",
        help="The default `timeout` (in seconds) for the `logot` fixture",
    )
    _add_option(
        parser,
        group,
        name="async_waiter",
        help="The default `async_waiter` for the `logot` fixture",
    )


@pytest.fixture()
def logot(
    logot_level: str | int,
    logot_logger: str | None,
    logot_timeout: float,
    logot_async_waiter: Callable[[], AsyncWaiter],
) -> Generator[Logot, None, None]:
    """
    An initialized `logot.Logot` instance with log capturing enabled.
    """
    logot = Logot(
        timeout=logot_timeout,
        async_waiter=logot_async_waiter,
    )
    with logot.capturing(level=logot_level, logger=logot_logger) as logot:
        yield logot


@pytest.fixture(scope="session")
def logot_level(request: pytest.FixtureRequest) -> str | int:
    """
    The level used for automatic log capturing.
    """
    return _get_option(request, name="level", parser=str, default=Logot.DEFAULT_LEVEL)


@pytest.fixture(scope="session")
def logot_logger(request: pytest.FixtureRequest) -> str | None:
    """
    The logger used for automatic log capturing.
    """
    return _get_option(request, name="logger", parser=str, default=Logot.DEFAULT_LOGGER)


@pytest.fixture(scope="session")
def logot_timeout(request: pytest.FixtureRequest) -> float:
    """
    The default `timeout` (in seconds) for the `logot` fixture.
    """
    return _get_option(request, name="timeout", parser=float, default=Logot.DEFAULT_TIMEOUT)


@pytest.fixture(scope="session")
def logot_async_waiter(request: pytest.FixtureRequest) -> Callable[[], AsyncWaiter]:
    """
    The default `async_waiter` for the `logot` fixture.
    """
    return _get_option(request, name="async_waiter", parser=resolve_name, default=Logot.DEFAULT_ASYNC_WAITER)


def get_qualname(name: str) -> str:
    return f"logot_{name}"


def get_optname(name: str) -> str:
    return f"--logot-{name.replace('_', '-')}"


def _add_option(parser: pytest.Parser, group: pytest.OptionGroup, *, name: str, help: str) -> None:
    qualname = get_qualname(name)
    parser.addini(qualname, default=MISSING, help=help)
    group.addoption(
        get_optname(name),
        default=MISSING,
        dest=qualname,
        metavar=name.upper(),
        help=help,
    )


def _get_option(request: pytest.FixtureRequest, *, name: str, parser: Callable[[str], T], default: T) -> T:
    qualname = get_qualname(name)
    # Try to get the value from the command line, followed by the config file.
    value: str = request.config.getoption(qualname, default=MISSING)
    if value is MISSING:
        value = request.config.getini(qualname)
        if value is MISSING:
            # Give up and return the default.
            return default
    # Parse and return the value.
    try:
        return parser(value)
    except Exception as ex:
        raise pytest.UsageError(f"Invalid {qualname}: {ex}")
