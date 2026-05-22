Projekt lokalnej aplikacji blogowej stworzonej w ramach przedmiotu: Integracja Systemów Informatycznych.

## Funkcjonalności - "moduł blogowy (Lab 2)"
- **System Postów:** Dodawanie, edycja i usuwanie wpisów przez Panel Admina.
- **Statusy:** Rozróżnienie między szkicem a opublikowanym postem.
- **Nowoczesny UI:** Responsywny interfejs zbudowany na Bootstrap 5 ze stylami CSS.
- **Testy Jednostkowe:** Zestaw testów sprawdzających poprawność modeli i widoków.
- **CI (Continuous Integration):** Automatyczne sprawdzanie kodu przez GitHub Actions przy każdym wypchnięciu zmian.

### Moduł Integracji API (Lab 3)
- **Open-Meteo Integration:** Dynamiczne pobieranie pogody dla Gdyni i innych (wybranych) miast Polski.
- **Wizualizacja danych:** Generowanie wykresów temperatury na 24h przy użyciu biblioteki **Matplotlib**.
- **JSON Data Processing:** Pobieranie i transformacja danych z JSONPlaceholder (filtrowanie, statystyki długości treści).
- **Własny Endpoint API:** Punkt dostępowy zwracający zagregowane dane pogodowe w formacie JSON.

### Moduł Konteneryzacji (Lab 4)
- **Pełna izolacja:** Aplikacja przygotowana do pracy w kontenerach Docker.
- **Orkiestracja:** Wykorzystanie Docker Compose do zarządzania stosem technologicznym.
- **Profesjonalna baza danych:** Przejście z SQLite na PostgreSQL.

### Automatyzacja CI/CD (Lab 5)
- **GitHub Actions:** Zautomatyzowany potok sprawdzający jakość kodu.
- **Linter (flake8):** Automatyczna kontrola stylu i składni Pythona.
- **Unit Testing:** Zestaw testów jednostkowych uruchamianych w chmurze przy każdym pushu.
- **Auto-Deploy:** Automatyczne wdrożenie na platformę **Render (PaaS)** po pomyślnym przejściu testów.
- **Cache:** Optymalizacja szybkości budowania potoku CI.


## Technologie
- Python / Django 
- Bootstrap 5 / Google Fonts
- SQLite (Baza lokalna), PostgreSQL
- Matplotlib (wizualizacja), Requests (pobieranie danych)
- Git / GitHub Actions
- Docker, Docker Compose
- Render