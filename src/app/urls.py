from django.urls import path

from . import views


urlpatterns = [
    path('', views.WeatherCityView.as_view(), name='weather_city'),
]
