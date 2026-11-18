"""Reusable function and method decorators."""
from __future__ import annotations

import functools
import inspect
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])
logger = logging.getLogger(__name__)


def timed(func: F) -> F:
    """Log elapsed wall-clock time of a function."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        started = time.perf_counter()
        result = func(*args, **kwargs)
        if inspect.isgenerator(result):
            def measured_generator():
                try:
                    yield from result
                finally:
                    logger.info("%s wykonano w %.6f s", func.__name__, time.perf_counter() - started)
            return measured_generator()
        try:
            return result
        finally:
            logger.info("%s wykonano w %.6f s", func.__name__, time.perf_counter() - started)
    return cast(F, wrapper)


def retry(attempts: int = 3, delay: float = 0.1) -> Callable[[F], F]:
    """Retry a function after exceptions; attempts includes the first call."""
    if attempts < 1 or delay < 0:
        raise ValueError("attempts >= 1 oraz delay >= 0 są wymagane")

    def decorate(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for number in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except (OSError, TimeoutError):
                    if number == attempts:
                        raise
                    time.sleep(delay)
        return cast(F, wrapper)
    return decorate


def requires_config(func: F) -> F:
    """Method decorator: checks the instance has a configured LogConfig."""
    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if getattr(self, "config", None) is None:
            raise RuntimeError("Obiekt nie ma konfiguracji")
        return func(self, *args, **kwargs)
    return cast(F, wrapper)
