"""Chunk-based file iterator."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator


class LogIterator(Iterator[str]):
    """Read a text file lazily in chunks, retaining only the current chunk."""

    def __init__(self, path: Path, chunk_size: int = 128, encoding: str = "utf-8") -> None:
        if chunk_size < 1:
            raise ValueError("chunk_size musi być dodatni")
        self.path = Path(path)
        self.chunk_size = chunk_size
        self.encoding = encoding
        self._file = None
        self._lines: list[str] = []

    def __iter__(self) -> "LogIterator":
        if self._file is None:
            self._file = self.path.open("r", encoding=self.encoding, errors="replace")
        return self

    def __next__(self) -> str:
        if self._file is None:
            self.__iter__()
        assert self._file is not None
        if not self._lines:
            self._lines = self._file.readlines(self.chunk_size)
        if not self._lines:
            self.close()
            raise StopIteration
        return self._lines.pop(0).rstrip("\n")

    def close(self) -> None:
        """Close the underlying file handle, if opened."""
        if self._file is not None:
            self._file.close()
            self._file = None

    def __enter__(self) -> "LogIterator":
        return iter(self)

    def __exit__(self, *_: object) -> None:
        self.close()
