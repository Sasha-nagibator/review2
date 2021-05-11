import datetime
import requests

from config import open_weather_token


def get_weather(city, open_weather_token):
    """
        Получает информацию о погоде с сайта openweathermap.org

        :param city: город, для которого ищет погоду
        :param open_weather_token: токен с сайта openweathermap.org

        :возвращает: город, температура, влажность, давление, восход солнца,
        закат солнца, продолжительность дня
    """
    ''' раскомментите если хотите проверить тут а не в тг
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    '''
    try:
        request = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid={open_weather_token}&units=metric"
        )
        data = request.json()

        city = data["name"]
        temp = round(data["main"]["temp"])

        ''' раскомментите если хотите проверить тут а не в тг
        weather_description = data["weather"][0]["main"]

        wd = code_to_smile[weather_description]
        '''
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime. \
            fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime. \
            fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = \
            datetime.datetime.fromtimestamp(data["sys"]["sunset"]) \
            - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # раскомментите если хотите проверить тут а не в тг
        '''print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {temp}°C {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\n
              Ветер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца:
               {sunset_timestamp}\n"
              f"Продолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня!"
              )'''

        return {'city': city, 'temp': temp, 'humidity': humidity,
                'pressure': pressure, 'wind': wind,
                'sunrise_timestamp': sunrise_timestamp,
                'sunset_timestamp': sunset_timestamp,
                'length_of_the_day': length_of_the_day}

    except Exception:
        # раскомментите если хотите проверить тут а не в тг
        # print("проверьте название города")
        return "Проверьте название города"


def main():
    """
    Получает погоду для введенного города

    """
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
