from __future__ import annotations

import logging


def to_levelno(level: int | str) -> int:
    # Handle `int` level.
    if isinstance(level, int):
        if logging.getLevelName(level).startswith("Level "):
            raise ValueError(f"Unknown level: {level!r}")
        return level
    # Handle `str` level.
    if isinstance(level, str):
        levelno = logging.getLevelName(level)
        if not isinstance(levelno, int):
            raise ValueError(f"Unknown level: {level!r}")
        return levelno
    # Handle invalid level.
    raise TypeError(f"Invalid level: {level!r}")


def to_logger(logger: logging.Logger | str | None) -> logging.Logger:
    # Handle `None` or `str` logger.
    if logger is None or isinstance(logger, str):
        return logging.getLogger(logger)
    # Handle `Logger` logger.
    if isinstance(logger, logging.Logger):
        return logger
    # Handle invalid logger.
    raise TypeError(f"Invalid logger: {logger!r}")


def to_timeout(timeout: float) -> float:
    # Handle valid timeout.
    if timeout >= 0.0:
        return timeout
    # Handle invalid timeout.
    raise ValueError(f"Invalid timeout: {timeout!r}")
