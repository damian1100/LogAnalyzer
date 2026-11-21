
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import perf_counter


def count_primes(limit: int) -> int:
    """count primes below limit"""
    if limit < 2:
        return 0
    count = 0
    for number in range(2, limit):
        is_prime = True
        divisor = 2
        while divisor * divisor <= number:
            if number % divisor == 0:
                is_prime = False
                break
            divisor += 1
        if is_prime:
            count += 1
    return count


def _timed_map(executor_kind: str, tasks: list[int]) -> tuple[float, list[int]]:
    started = perf_counter()
    if executor_kind == "sequential":
        results = [count_primes(value) for value in tasks]
    elif executor_kind == "threads":
        with ThreadPoolExecutor() as pool:
            results = list(pool.map(count_primes, tasks))
    elif executor_kind == "processes":
        with ProcessPoolExecutor() as pool:
            results = list(pool.map(count_primes, tasks))
    else:
        raise ValueError(f"Nieznany tryb: {executor_kind}")
    return perf_counter() - started, results


def run_benchmark(tasks: int = 4, workload: int = 35000) -> dict[str, object]:
    """run equal CPU workloads sequentially"""
    if tasks < 1 or workload < 2:
        raise ValueError("tasks >= 1 i workload >= 2 są wymagane")
    inputs = [workload] * tasks
    results: dict[str, object] = {"tasks": tasks, "workload_limit": workload, "seconds": {}}
    expected = None
    for mode in ("sequential", "threads", "processes"):
        elapsed, output = _timed_map(mode, inputs)
        if expected is None:
            expected = output
        elif output != expected:
            raise RuntimeError("Różne wyniki benchmarku – pomiar niewiarygodny")
        results["seconds"][mode] = round(elapsed, 6)  # type: ignore[index]
    return results
