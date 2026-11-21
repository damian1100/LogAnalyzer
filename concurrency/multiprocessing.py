"""CPU bound aggregation"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from core.analyzer import analyze_records
from core.config import LogConfig
from core.parser import parse_file


def _analyze_one_file(path_text: str, max_size: int, strict: bool) -> dict[str, object]:
    records = list(parse_file(Path(path_text), LogConfig(max_size, strict)))
    return analyze_records(records)


def analyze_in_processes(
    paths: list[Path], max_workers: int = 4, config: LogConfig | None = None
) -> list[dict[str, object]]:
    if max_workers < 1:
        raise ValueError("max_workers musi być dodatni")
    config = config or LogConfig()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_analyze_one_file, str(Path(path)), config.max_file_size_mb, config.strict)
            for path in paths
        ]
        return [future.result() for future in futures]
