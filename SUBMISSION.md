# Informacja o projekcie

**Nazwa:** LogAnalyzer – analizator logów serwera WWW

**Opis:** Aplikacja w Pythonie 3.12+ odczytuje pliki logów, parsuje wpisy z użyciem wyrażeń regularnych, generuje statystyki ruchu i błędów HTTP oraz demonstruje iterator, generatory, dekoratory, wątki, procesy i wpływ GIL.

**Repozytorium:** 

**Lokalizacja kodu:** gałąź `main`, katalog główny repozytorium. Instrukcja uruchomienia i tabela mapowania wymagań znajdują się w `README.md`.

**Uruchomienie testów:** `python -m unittest discover -s tests -v`

**Uruchomienie aplikacji:** `python main.py analyze data/access.log data/error.log --parallel threads`

