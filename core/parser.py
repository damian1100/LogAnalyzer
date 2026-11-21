
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterator

from core.config import LogConfig
from core.reader import LogIterator
from utils.decorators import requires_config, timed
from utils.patterns import ACCESS_LOG_RE, is_valid_ipv4

logger = logging.getLogger(__name__)


class LogParser:


    def __init__(self, config: LogConfig) -> None:
        self.config = config

    @requires_config
    def parse_line(self, line: str) -> dict[str, object] | None:
        match = ACCESS_LOG_RE.search(line)
        if not match:
            return None
        data = match.groupdict()
        if not is_valid_ipv4(data["ip"]):
            return None
        try:
            status = int(data["status"])
            size = 0 if data["size"] == "-" else int(data["size"])
        except ValueError:
            return None
        return {
            "ip": data["ip"], "timestamp": data["timestamp"], "method": data["method"],
            "url": data["url"], "status": status, "size": size,
        }


@timed
def parse_file(path: Path, config: LogConfig | None = None) -> Iterator[dict[str, object]]:

    config = config or LogConfig()
    path = Path(path)
    size_limit = config.max_file_size_mb * 1024 * 1024
    if path.stat().st_size > size_limit:
        raise ValueError(f"Plik {path} przekracza limit {config.max_file_size_mb} MiB")
    parser = LogParser(config)
    with LogIterator(path) as lines:
        for line_number, line in enumerate(lines, start=1):
            record = parser.parse_line(line)
            if record is None:
                if config.strict:
                    raise ValueError(f"Niepoprawny wpis w {path}, linia {line_number}")
                logger.debug("Pominięto niepoprawną linię %s:%d", path, line_number)
                continue
            yield record


def parse_lines(lines: Iterator[str], config: LogConfig | None = None) -> Iterator[dict[str, object]]:

    parser = LogParser(config or LogConfig())
    for line in lines:
        record = parser.parse_line(line)
        if record is not None:
            yield record
