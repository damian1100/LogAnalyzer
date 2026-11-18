# LogAnalyzer – analizator logów serwera WWW

Aplikacja CLI w Pythonie 3.12+ do leniwej analizy logów dostępu w formacie zbliżonym do Apache Common Log Format. Raportuje liczbę żądań, błędy HTTP, udział błędów, transfer danych, najczęstsze adresy IP i endpointy.

## Funkcje
- parsowanie wpisów logów przy użyciu regexów z nazwanymi grupami;
- iterator pliku i generatory – dane są przetwarzane leniwie;
- dekoratory pomiaru czasu, ponawiania i kontroli konfiguracji metody;
- współbieżny odczyt wielu plików w wątkach z blokadą `Lock`;
- osobne procesy do CPU-bound analizy plików;
- benchmark GIL: wykonanie sekwencyjne, wątki, procesy;
- CLI, logging, JSON i testy `unittest`.

## Uruchomienie
Wymagany Python 3.12 lub nowszy. Brak zewnętrznych zależności.

```bash
python --version
python main.py analyze data/access.log data/error.log --parallel threads
python main.py analyze data/access.log --parallel sequential --output reports.json
python main.py analyze data/access.log data/error.log --parallel processes --workers 2
python main.py benchmark --tasks 4 --workload 35000
python -m unittest discover -s tests -v
```

Na Windows uruchamianie procesów jest zabezpieczone przez `if __name__ == "__main__"` w `main.py`. Przy pierwszym benchmarku warto zacząć od mniejszego `--workload`.

## Mapowanie wymagań na kod

| Zagadnienie | Plik / klasa / funkcja |
|---|---|
| Dekorator bez parametrów | `utils/decorators.py` → `timed` |
| Dekorator z parametrami | `utils/decorators.py` → `retry(attempts, delay)` |
| `functools.wraps` | `utils/decorators.py` → wszystkie dekoratory |
| Dekorator metody z `self` | `utils/decorators.py` → `requires_config`; użycie w `core/parser.py` |
| `@property` i setter | `core/config.py` → `LogConfig.max_file_size_mb` |
| `@classmethod` | `core/config.py` → `LogConfig.from_dict` |
| `@staticmethod` | `core/config.py` → `LogConfig.is_supported_encoding` |
| Iterator | `core/reader.py` → `LogIterator.__iter__`, `__next__` |
| Generator `yield` | `core/parser.py` → `parse_file`, `parse_lines` |
| Wyrażenie generujące | `main.py` → `[record for path ... for record in parse_file(...)]` |
| Regex i nazwane grupy | `utils/patterns.py` → `ACCESS_LOG_RE`, `EMAIL_RE`, `DATE_RE` |
| Wątki I/O | `concurrency/threaded.py` → `ThreadPoolExecutor` |
| Synchronizacja | `concurrency/threaded.py` → `Lock` |
| Procesy | `concurrency/multiprocessing.py` → `ProcessPoolExecutor` |
| Pomiar GIL | `benchmarks/gil_benchmark.py` → `run_benchmark` |

## Benchmark i GIL

Uruchom benchmark na docelowym komputerze i wklej rzeczywiste wyniki do tabeli poniżej. Nie należy wpisywać wyników z innego komputera, ponieważ czas zależy m.in. od CPU, systemu operacyjnego, obciążenia i liczby rdzeni.

| Tryb | Czas [s] |
|---|---:|
| Sekwencyjnie | uzupełnij po uruchomieniu |
| Wątki | uzupełnij po uruchomieniu |
| Procesy | uzupełnij po uruchomieniu |

**Wnioski dotyczące GIL (do skonfrontowania z własnym pomiarem):** Benchmark wykonuje obliczenia CPU-bound w czystym Pythonie, dlatego w standardowym buildzie CPythona GIL ogranicza wykonywanie bytecode przez wiele wątków jednocześnie. W efekcie wątki zwykle nie przyspieszają tego rodzaju obciążenia, a narzut przełączania może nawet pogorszyć wynik. Procesy mają osobne interpretery i osobne GIL-e, więc mogą wykonywać obliczenia równolegle na wielu rdzeniach. Procesy ponoszą jednak koszt uruchomienia, serializacji argumentów i przekazywania wyników. Dla małych zadań sekwencyjne wykonanie może być najszybsze. Dla operacji I/O-bound wątki są przydatne, ponieważ mogą wykonywać inne zadania podczas oczekiwania na dysk lub sieć. Wnioski należy opisać na podstawie tabeli z własnego komputera, a nie zakładać, że procesy zawsze wygrają.

## Problemy napotkane podczas realizacji
Przykładowe zagadnienia do opisania po implementacji:
- różne formaty wpisów logów i konieczność pomijania niepoprawnych linii;
- ograniczenie pamięci przez przetwarzanie strumieniowe;
- bezpieczeństwo współdzielonej listy wyników w wątkach;
- wymóg funkcji najwyższego poziomu i danych możliwych do serializacji w `ProcessPoolExecutor`;
- narzut procesów przy krótkich zadaniach benchmarkowych.

## Ograniczenia
Parser obsługuje typowy format dostępu Apache, a nie dowolny format logów. Weryfikacja IPv4 obejmuje zakres oktetów. Przykładowe pliki są syntetyczne i nie zawierają danych osobowych. Moduł `EMAIL_RE` pokazuje ekstrakcję adresów e-mail, ale analiza dostępu nie wymaga ich obecności.

## Propozycja prezentacji (10 minut)
1. 1 min – cel i format danych.
2. 2 min – `LogIterator`, generator i regex.
3. 2 min – dekoratory oraz konfiguracja.
4. 2 min – wątki, `Lock` i procesy.
5. 2 min – uruchomienie benchmarku i interpretacja GIL.
6. 1 min – testy, ograniczenia i wnioski.
