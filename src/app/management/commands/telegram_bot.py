import httpx
import telebot
from django.conf import settings
from django.core.management import BaseCommand
from django.urls import reverse
from telebot import types
from telebot.formatting import format_text


bot = telebot.TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


def gen_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Узнать погоду", callback_data="find_weather"))
    return keyboard


def get_text(data):
    return format_text(f'Температура (°C) - ({data.get("temp")})\n'
                       f'Скорость ветра (в м/с) - ({data.get("wind_speed")})',
                       f'Давление (в мм рт. ст.) - ({data.get("pressure_mm")})\n\n',)


def get_data(message):
    with httpx.Client(params={'city': message.text}) as client:
        response = client.get(f'{settings.CURRENT_HOST}{reverse("weather_city")}')
        if response.status_code == 200:
            return response.json().get('data')


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(chat_id=message.chat.id, text="Укажите наименование города")


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    data = get_data(message)
    if data:
        bot.send_message(chat_id=message.chat.id, text=message.text, reply_markup=gen_keyboard())
    else:
        bot.send_message(chat_id=message.chat.id, text="Данного города не существует попробуйте еще раз")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "find_weather":
                bot.send_message(chat_id=call.message.chat.id, text=get_text(get_data(call.message)))
                bot.send_message(chat_id=call.message.chat.id, text=call.message.text, reply_markup=gen_keyboard())
    except Exception as e:
        print(repr(e))


class Command(BaseCommand):

    help = 'Телеграм бот'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

