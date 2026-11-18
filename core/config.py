"""Validated application configuration."""
from __future__ import annotations


class LogConfig:
    """Configuration with a validated property setter."""

    def __init__(self, max_file_size_mb: int = 50, strict: bool = False) -> None:
        self.max_file_size_mb = max_file_size_mb
        self.strict = strict

    @property
    def max_file_size_mb(self) -> int:
        """Maximum accepted input file size in MiB."""
        return self._max_file_size_mb

    @max_file_size_mb.setter
    def max_file_size_mb(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("max_file_size_mb musi być dodatnią liczbą całkowitą")
        self._max_file_size_mb = value

    @classmethod
    def from_dict(cls, values: dict[str, object]) -> "LogConfig":
        """Create configuration from a dictionary."""
        allowed = {"max_file_size_mb", "strict"}
        unknown = set(values) - allowed
        if unknown:
            raise ValueError(f"Nieznane ustawienia: {', '.join(sorted(unknown))}")
        return cls(**values)  # type: ignore[arg-type]

    @staticmethod
    def is_supported_encoding(name: str) -> bool:
        """Small static helper used by the CLI/tests."""
        import codecs
        try:
            codecs.lookup(name)
            return True
        except LookupError:
            return False
