from asgiref.sync import sync_to_async
from django.db import models, OperationalError


class WeatherCityModel(models.Model):

    city_name = models.CharField(unique=True, max_length=255, verbose_name='Название города')
    lat = models.FloatField(verbose_name='Широта (в градусах)')
    lon = models.FloatField(verbose_name='Долгота (в градусах)')
    temp = models.SmallIntegerField(blank=True, null=True, verbose_name='Температура (°C)')
    wind_speed = models.FloatField(blank=True, null=True, verbose_name='Скорость ветра (в м/с)')
    pressure_mm = models.SmallIntegerField(blank=True, null=True, verbose_name='Давление (в мм рт. ст.)')
    is_pending = models.BooleanField(default=False, verbose_name='Находится в ожидании повтора')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'<{self.city_name}>'

    def update_pending(self):
        """- все данные Находящиеся в ожидании повтора """
        try:
            WeatherCityModel.objects.filter(is_pending=True).update(is_pending=False)
        except OperationalError as ex:
            print(ex)

    @sync_to_async
    def get_instance(cls, kwargs):
        """- получить экземпляр объекта """
        try:
            return WeatherCityModel.objects.get(**kwargs)
        except Exception as ex:
            print(ex)

    def switch_pending(self, _bool):
        """- сохранить данные """
        self.is_pending = _bool
        self.save()

    @sync_to_async
    def update_field(self, kwargs):
        """- сохранить данные """
        self.__dict__.update(**kwargs)
        self.save()

    class Meta:
        verbose_name = 'Погода'
        verbose_name_plural = 'Погоды'

