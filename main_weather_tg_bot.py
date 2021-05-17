import datetime
import pandas as pd
import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import tg_bot_token, open_weather_token
from peewee import DateField, FloatField, IntegerField, Model, SqliteDatabase

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Отвечает на команду /start

    """

    await message.reply("Привет! Напиши мне название города и я пришлю сводку"
                        "погоды!"
                        " Или напиши /stats и я пришлю статистику погоды"
                        "в Москве за последнее время!")


@dp.message_handler(commands=["stats"])
async def stats(message: types.Message):
    """
    Выводит статистику погоды в Мосвае за последнее время.
    Данные читает из базы данных

    """
    small_difference = 5
    nothing = 0
    data = pd.read_csv('RU.csv')
    max_temp = data['temp'].max()
    max_temp_time = data[data['temp'] == max_temp]["time_local"].values[0]
    max_prcp = data['prcp'].max()
    min_wind = data['wspd'].min()
    max_prcp_time = data[data['prcp'] == max_prcp]["time_local"].values[0]
    best_weather = data[(data['temp'] > max_temp - small_difference) &
                        (data['prcp'] == nothing) &
                        (data['wspd'] < min_wind + small_difference)].values

    db = SqliteDatabase('Weather.db')

    class Data(Model):
        name = FloatField()
        weather_conditions = FloatField()
        day = DateField()

        class Meta:
            database = db

    class SuperWeather(Model):
        wind = FloatField()
        temp = FloatField()
        prcp = IntegerField()
        day = DateField()

        class Meta:
            database = db

    db.connect()
    db.create_tables([Data, SuperWeather])

    high_temp = Data(name='highest temperature', weather_conditions=max_temp,
                     day=max_temp_time)
    high_temp.save()
    high_prcp = Data(name='max precipitation', weather_conditions=max_prcp,
                     day=max_prcp_time)
    high_prcp.save()

    time_place = 1
    temp_place = 2
    wind_place = 8
    for elem in best_weather:
        line = SuperWeather(temp=elem[temp_place], day=elem[time_place],
                            wind=elem[wind_place], prcp=0)
        line.save()
    for string in Data.select():
        str_to_print = f"{string.name}: {string.weather_conditions} в" \
                       f"{string.day}"
        await bot.send_message(message.from_user.id, str_to_print)
    for line in SuperWeather.select():
        str_to_print = f"в {line.day} темп {line.temp}, ветер {line.wind}," \
                       f"осадки {line.prcp}"
        await bot.send_message(message.from_user.id, str_to_print)

    db.close()


@dp.message_handler()
async def get_weather(message: types.Message):
    """
            Получает информацию о погоде с сайта openweathermap.org

            :param message: сообщение с названием города

    """

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        request = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}"
            f"&appid={open_weather_token}&units=metric"
        )
        data = request.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]

        wd = code_to_smile[weather_description]

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime. \
            fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime. \
            fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime. \
            fromtimestamp(data["sys"]["sunset"]) - datetime.datetime. \
            fromtimestamp(data["sys"]["sunrise"])

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        await message.reply(f"{current_time}\n"
                            f"Погода в городе: {city}\nТемпература:"
                            f" {cur_weather}°C {wd}\n"
                            f"Влажность: {humidity}%\nДавление:"
                            f" {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат"
                            f" солнца: {sunset_timestamp}\nПродолжительность "
                            f"дня: {length_of_the_day}\n "
                            f"***Хорошего дня!***"
                            )

    except Exception:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)
