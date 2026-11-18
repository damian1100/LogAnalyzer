"""Command-line entry point for LogAnalyzer."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from core.analyzer import analyze_records, merge_reports
from core.parser import parse_file
from concurrency.threaded import parse_files_concurrently
from concurrency.multiprocessing import analyze_in_processes
from benchmarks.gil_benchmark import run_benchmark
from core.config import LogConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analizator logów serwera WWW")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analizuj jeden lub wiele plików logów")
    analyze.add_argument("files", nargs="+", type=Path)
    analyze.add_argument("--workers", type=int, default=4)
    analyze.add_argument("--parallel", choices=("threads", "processes", "sequential"), default="threads")
    analyze.add_argument("--output", type=Path, help="Opcjonalny plik JSON")

    bench = sub.add_parser("benchmark", help="Porównaj wykonanie sekwencyjne, wątki i procesy")
    bench.add_argument("--tasks", type=int, default=4)
    bench.add_argument("--workload", type=int, default=35000)

    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()

    if args.command == "benchmark":
        results = run_benchmark(tasks=args.tasks, workload=args.workload)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    config = LogConfig()
    config.max_file_size_mb = 100
    for path in args.files:
        if not path.is_file():
            raise SystemExit(f"Nie znaleziono pliku: {path}")

    if args.parallel == "threads":
        records = parse_files_concurrently(args.files, max_workers=args.workers, config=config)
    elif args.parallel == "processes":
        partial_reports = analyze_in_processes(args.files, max_workers=args.workers, config=config)
        report = merge_reports(partial_reports)
        records = None
    else:
        records = [record for path in args.files for record in parse_file(path, config)]

    if args.parallel != "processes":
        report = analyze_records(records or [])
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        logging.info("Zapisano raport: %s", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
