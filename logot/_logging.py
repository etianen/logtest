from __future__ import annotations

import logging

from logot._capture import Captured
from logot._logot import Capturer, Logot


class LoggingCapturer(Capturer):
    __slots__ = ("_logger", "_handler", "_prev_levelno")

    def start_capturing(self, logot: Logot, /, *, level: str | int, logger: str | None) -> None:
        logger = self._logger = logging.getLogger(logger)
        handler = self._handler = _Handler(level, logot)
        # If the logger is less verbose than the handler, force it to the necessary verboseness.
        self._prev_levelno = logger.level
        if handler.level < logger.level:
            logger.setLevel(handler.level)
        # Add the handler.
        logger.addHandler(handler)

    def stop_capturing(self) -> None:
        # Remove the handler and restore the previous level.
        self._logger.removeHandler(self._handler)
        self._logger.setLevel(self._prev_levelno)


class _Handler(logging.Handler):
    __slots__ = ("_logot",)

    def __init__(self, level: str | int, logot: Logot) -> None:
        super().__init__(level)
        self._logot = logot

    def emit(self, record: logging.LogRecord) -> None:
        captured = Captured(record.levelname, record.getMessage(), levelno=record.levelno)
        self._logot.capture(captured)
