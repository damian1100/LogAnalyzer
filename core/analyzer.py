"""aggregation of parsed web-server records"""
from __future__ import annotations

from collections import Counter
from typing import Iterable


def analyze_records(records: Iterable[dict[str, object]]) -> dict[str, object]:
    """compute request, status, endpoint, client summaries"""
    status_counts: Counter[int] = Counter()
    ip_counts: Counter[str] = Counter()
    url_counts: Counter[str] = Counter()
    methods: Counter[str] = Counter()
    total_bytes = 0
    total = 0
    for record in records:
        total += 1
        status_counts[int(record["status"])] += 1
        ip_counts[str(record["ip"])] += 1
        url_counts[str(record["url"])] += 1
        methods[str(record["method"])] += 1
        total_bytes += int(record["size"])
    errors = sum(count for status, count in status_counts.items() if status >= 400)
    return {
        "total_requests": total,
        "error_requests": errors,
        "error_rate_percent": round(errors / total * 100, 2) if total else 0.0,
        "total_bytes": total_bytes,
        "status_codes": dict(sorted(status_counts.items())),
        "methods": dict(methods.most_common()),
        "top_ips": ip_counts.most_common(10),
        "top_urls": url_counts.most_common(10),
    }


def merge_reports(reports: Iterable[dict[str, object]]) -> dict[str, object]:
    """merge partial reports produced independently"""
    status_counts: Counter[int] = Counter()
    ip_counts: Counter[str] = Counter()
    url_counts: Counter[str] = Counter()
    methods: Counter[str] = Counter()
    total = errors = total_bytes = 0
    for report in reports:
        total += int(report["total_requests"])
        errors += int(report["error_requests"])
        total_bytes += int(report["total_bytes"])
        status_counts.update({int(k): int(v) for k, v in dict(report["status_codes"]).items()})
        methods.update({str(k): int(v) for k, v in dict(report["methods"]).items()})
        ip_counts.update({str(ip): int(count) for ip, count in report["top_ips"]})
        url_counts.update({str(url): int(count) for url, count in report["top_urls"]})
    return {
        "total_requests": total,
        "error_requests": errors,
        "error_rate_percent": round(errors / total * 100, 2) if total else 0.0,
        "total_bytes": total_bytes,
        "status_codes": dict(sorted(status_counts.items())),
        "methods": dict(methods.most_common()),
        "top_ips": ip_counts.most_common(10),
        "top_urls": url_counts.most_common(10),
    }
