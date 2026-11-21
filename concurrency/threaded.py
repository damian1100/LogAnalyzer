
from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

from core.config import LogConfig
from core.parser import parse_file

logger = logging.getLogger(__name__)


def parse_files_concurrently(
    paths: list[Path], max_workers: int = 4, config: LogConfig | None = None
) -> list[dict[str, object]]:
    """parse multiple files concurrently"""
    if max_workers < 1:
        raise ValueError("max_workers musi być dodatni")
    config = config or LogConfig()
    results: list[dict[str, object]] = []
    lock = Lock()

    def worker(path: Path) -> None:
        local_records = list(parse_file(path, config))
        with lock:
            results.extend(local_records)
        logger.info("Wątek zakończył plik %s (%d rekordów)", path, len(local_records))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, Path(path)) for path in paths]
        for future in as_completed(futures):
            future.result()  # propagate worker exceptions to caller
    return results
