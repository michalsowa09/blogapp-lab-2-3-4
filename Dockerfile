#Używam oficjalnego obrazu Pythona w wersji slim (lekka):
FROM python:3.11-slim

#Ustawiam zmienne środowiskowe Pythona, żeby nie śmiecił skompilowanym kodem bajtowym i żeby logi były od razu w konsoli (a nie w buforze):

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Ustawiam katalog roboczy w folderze app:
WORKDIR /app

#Instaluje zależności systemowe (potrzebne między innymi do kompilacji niektórych bibliotek):
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

#Najpierw kopiuję tylko requirements.txt, żeby docker mógł zbuforować instalację bibliotek:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Kopiuje resztę plików do projektu kontenera:

COPY . .

#Komenda uruchamiająca serwer - włączam nasłuchiwanie systemowe na interfejsie 0.0.0.0 - port 8000:

CMD["python", "manage.py", "runserver", "--host", "0.0.0.0", "--port", "8000", "--reload"]

