from __future__ import annotations

import logging

import pytest

from logot import Logot, logged
from tests import lines, logger


def test_capturing() -> None:
    assert logger.level == logging.NOTSET
    # Set a fairly non-verbose log level.
    logger.setLevel(logging.WARNING)
    try:
        with Logot().capturing(level=logging.DEBUG, logger=logger) as logot:
            assert isinstance(logot, Logot)
            # The logger will have been overridden for the required verbosity.
            assert logger.level == logging.DEBUG
        # When the capture ends, the logging verbosity is restored.
        assert logger.level == logging.WARNING
    finally:
        # Whatever this test does, reset the logger to what it was!
        logger.setLevel(logging.NOTSET)


def test_assert_logged_pass(logot: Logot) -> None:
    logger.info("foo bar")
    logot.assert_logged(logged.info("foo bar"))


def test_asset_logged_fail(logot: Logot) -> None:
    with pytest.raises(AssertionError) as ex:
        logot.assert_logged(logged.info("foo bar"))
    assert str(ex.value) == lines(
        "Not logged:",
        "",
        "[INFO] foo bar",
    )
