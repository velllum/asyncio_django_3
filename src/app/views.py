import asyncio
from time import sleep

import httpx
from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import classonlymethod
from django.views import generic

from . import models


class WeatherCityView(generic.View):
    """- Погода """
    _model = models.WeatherCityModel

    _model().update_pending()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._context = {}
        self._data = None
        self._instance = None
        self._json_data = None
        self._kwargs_data = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._city_name = self.request.GET.get('city')

    async def get(self, *args, **kwargs):
        """- переопределить GET запрос """
        self._instance = await self._model.get_instance({'city_name': self._city_name})

        if not self._instance:
            self._context.update({'message': f'Данных о текущем городе <{self._city_name}> нет в базе'})

        elif self._instance.is_pending:
            await self._get_kwargs_data(self._instance.__dict__)
            self._context.update({'data': self._kwargs_data})

        else:
            await self._run_timing_event()
            await self._get_json_data()
            await self._get_kwargs_data(self._json_data.get('fact'))
            await self._instance.update_field(self._kwargs_data)
            self._context.update({'data': self._kwargs_data})

        return JsonResponse(self._context)

    async def _get_json_data(self):
        """- получить ответ """
        async with httpx.AsyncClient(params={'lat': self._instance.lat, 'lon': self._instance.lon, 'lang': ['ru_RU']},
                                     headers={'X-Yandex-API-Key': settings.YANDEX_WEATHER_API_KEY}) as client:
            response = await client.get(settings.YANDEX_WEATHER_API_URL)
            if  response.status_code == 200:
                self._json_data = response.json()

    async def _run_timing_event(self):
        """- запустить событие таймаута """
        loop = asyncio.get_event_loop()
        async_function = sync_to_async(self._thread_handler, thread_sensitive=False)
        loop.create_task(async_function(settings.YANDEX_WEATHER_TIMING, self._instance))

    async def _get_kwargs_data(self, kw):
        """- получить словарь сданными """
        self._kwargs_data = {'temp': kw.get('temp'), 'wind_speed': kw.get('wind_speed'),
                             'pressure_mm': kw.get('pressure_mm'),}

    @classmethod
    def _thread_handler(cls, timing, instance):
        """- обработчик """
        instance.switch_pending(True)
        sleep(int(timing))
        print(f'***** sleep <{timing}> ******')
        instance.switch_pending(False)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """- переопределить процесс запроса """
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

