import requests
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render
from django.http import JsonResponse

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


def json_placeholder_view(request):
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()  # To są posty pobrane z internetu

        # OBRÓBKA DANYCH (Wymaganie laboratorium):
        # 1. Filtrowanie: biorę tylko posty użytkownika o ID = 1 (z 100 dostępnych)
        user_1_posts = [p for p in data if p['userId'] == 1]

        # 2. Statystyki: Liczę średnią długość tytułu dla WSZYSTKICH postów z API
        total_posts = len(data)
        avg_title_len = sum(len(p['title']) for p in data) / total_posts

        context = {
            'external_posts': user_1_posts[:5],  #Pokaże 5 postów usera nr 1
            'total_api_posts': total_posts,
            'avg_title_length': round(avg_title_len, 2),
            'user_id': 1
        }
        return render(request, 'external_data/json_data.html', context)

    except Exception as e:
        return render(request, 'external_data/error.html', {'error': str(e)})


def weather_summary_api(request):
    """
    Mój własny endpoint API, który pobiera surowe dane z Open-Meteo,
    agreguje je (liczy średnią) i zwraca gotowy raport w formacie JSON.
    """
    #Współrzędne Gdyni
    url = "https://api.open-meteo.com/v1/forecast?latitude=54.5189&longitude=18.5305&hourly=temperature_2m"

    try:
        response = requests.get(url)
        data = response.json()

        # OBRÓBKA DANYCH (Agregacja):
        # Pobieram temperatury na najbliższe 24h
        temps = data['hourly']['temperature_2m'][:24]

        #Obliczam statystyki
        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)

        #Tworze własną strukturę odpowiedzi JSON
        report = {
            'metadata': {
                'city': 'Gdynia',
                'provider': 'Moja Aplikacja Django - Lab 3',
                'description': 'Dobowa analiza temperatury'
            },
            'stats': {
                'average_temp': round(avg_temp, 2),
                'max_temp': max_temp,
                'min_temp': min_temp,
                'unit': 'Celsius'
            },
            'raw_data_preview': temps[:5]  #Pokazuje próbkę surowych danych
        }

        return JsonResponse(report)  #Zwracam "czyste" dane, nie stronę HTML

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)