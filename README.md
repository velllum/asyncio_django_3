## Сервис по работе с API яндекс погодой


## Ссылки представлений
- **[GET] ../weather?city=<city_name>** - получить список всех пользователей

Клонировать проект из репозитория

`git clone https://github.com/velllum/test_site-4you.git`

## Установка через pip, pipenv

Запустить установку зависимостей любым способов

`pip install -r requirements.txt`

`pipenv install -r requirements.txt`

После установки запустить приложение командой, из корневой директории 

`./manager runserver`

Запустить telegram bot командой, из корневой директории 

`./manager telegram_bot`

Создать админ пользователя командой, из корневой директории

`./manager createsuperuser`

Создать миграции базы данных командой, из корневой директории

`./manager makemigrations`

`./manager migrate`

После миграции пройдите в админ панел приложения,
по адресу ../admin в разделе Города->Погоды укажите наименование города и координаты широты и долготы

Создайте файл .env и укажите в нем переменные 

`SECRET_KEY='<секретный ключ>'`

`DEBUG=<True или False>`

`CURRENT_HOST='<Веб хост пример http://127.0.0.1:8000>'`

`YANDEX_WEATHER_API_KEY='<секретный токен>' - получить можно тут https://yandex.ru/dev/weather/`

`YANDEX_WEATHER_API_URL='https://api.weather.yandex.ru/v2/forecast' - ссылка API яндекс погоды для получения данных`

`YANDEX_WEATHER_TIMING=<время таймаута по умолчанию указывается в секундах 1800 сек = 30 мин>`

`TELEGRAM_BOT_API_KEY='<секретный токен бота, получить можно при регистрации телеграм бота>'`
