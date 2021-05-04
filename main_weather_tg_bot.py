import datetime
import pandas as pd
import requests
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

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

    data = pd.read_csv('RU.csv')
    max_temp = data['temp'].max()
    avg_pressure = data['pres'].mean()
    max_temp_time = data[(data['temp'] == max_temp)]["time_local"].values[0]
    max_prcp = data['prcp'].max()
    min_wind = data['wspd'].min()
    max_prcp_time = data[(data['prcp'] == max_prcp)]["time_local"].values[0]
    best_weather = data[(data['temp'] > max_temp - 3) & (data['prcp'] == 0) &
                        (data['wspd'] < min_wind + 6)].values

    await message.reply(f"максимальная температура была {max_temp},"
                        f"это было в {max_temp_time}")

    await bot.send_message(message.from_user.id, f"среднее давление за это"
                                                 f"время {avg_pressure}")
    await bot.send_message(message.from_user.id, f"больше всего осадков было"
                                                 f"{max_prcp}, это было в"
                                                 f"{max_prcp_time}")

    await bot.send_message(message.from_user.id, "самая комфортная погода"
                                                 "была в:")
    for elem in best_weather:
        str_to_print = f"в {elem[1]} температура была {elem[2]}, осадков не" \
                       f"было, скорость ветра была {elem[8]} м/с"
        await bot.send_message(message.from_user.id, str_to_print)


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
        sunrise_timestamp = datetime.datetime.\
            fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.\
            fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.\
            fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.\
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
