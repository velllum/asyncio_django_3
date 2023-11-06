from django.contrib import admin

from . import models


@admin.register(models.WeatherCityModel)
class WeatherCityModelAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'city_name',)
    list_display = ('id', 'city_name', 'lat', 'lon', 'temp', 'wind_speed', 'pressure_mm', 'is_pending',
                    'created_date', 'updated_date',)
    ordering = ('id', 'city_name',)
    list_filter = ('city_name',)
    search_fields = ('city_name',)

