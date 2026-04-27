from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_view, name='weather_page'),
    path('json-stats/', views.json_placeholder_view, name='json_stats'),
    path('api/weather-summary/', views.weather_summary_api, name='weather_api'),
]