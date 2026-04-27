import requests
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render

#Słownik z miastami i ich współrzędnymi (wybrałem: Gdynia, Gdańsk, Warszawa, Kraków):

CITIES = {
    "Gdynia": {"lat": 54.5189, "lon": 18.5305},
    "Gdańsk": {"lat": 54.3520, "lon": 18.6464},
    "Warszawa": {"lat": 52.2297, "lon": 21.0122},
    "Kraków": {"lat": 50.0647, "lon": 19.9450}
}

def weather_view(request):
    #Pobieram nazwę miasta z zapytania - jeśli nie ma, domyślnie Gdynia:
    selected_city = request.GET.get("city", "Gdynia")
    coords = CITIES.get(selected_city, CITIES["Gdynia"])

    #1. Pobieranie danych z API Open-Meteo:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&hourly=temperature_2m"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        #Obróbka danych (najbliższe 24 godziny):
        all_times = data['hourly']['time'][:24]
        all_temps = data['hourly']['temperature_2m'][:24]

        #Wyciągam same godziny bez dat (dla lepszego wyglądu na wykresie):
        hours = [t.split("T")[1] for t in all_times] #Tu jest list comprehension
        current_temp = all_temps[0]

        #Wizualizacja - wykres Matplotlib:
        plt.switch_backend('Agg') #Ważne dla serwerów webowych
        plt.figure(figsize=(10, 5))
        plt.plot(hours, all_temps, marker='o', color='#3498db', linewidth=2)
        plt.fill_between(hours, all_temps, color='#3498db', alpha=0.1)  #Ładne wypełnienie

        plt.title(f'Prognoza temperatury dla: {selected_city} (24h)', fontsize=15)
        plt.xlabel('Godzina')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()

        #Konwersja wykresu do Base64 (żeby wyświetlić bezpośrednio w HTML)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        plt.close()  #Zamykam wykres, żeby nie zjadał pamięci

        context = {
            'chart': uri,
            'current_temp': current_temp,
            'selected_city': selected_city,
            'cities': CITIES.keys()  #Lista miast do formularza
        }
        return render(request, 'external_data/weather.html', context)

    except Exception as e:
        return render(request, 'external_data/weather.html', {'error': str(e)})