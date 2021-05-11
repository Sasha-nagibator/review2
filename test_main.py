import unittest

from config import open_weather_token
from main import get_weather


class Test_get_weather(unittest.TestCase):

    def test_CityNotExist(self):
        """
        Проверяет корректность работы функции get_weather,
        если город введен некорректно

        """
        self.assertEqual(get_weather("fsdfasgsdf", open_weather_token),
                         "Проверьте название города")
        self.assertEqual(get_weather("1", open_weather_token),
                         "Проверьте название города")

    def test_TempCheck(self):
        """
        Проверяет корректность работы функции get_weather
        (что правильно выводит температуру)

        """
        extrimely_cold = -50

        self.assertGreater(get_weather("Riga", open_weather_token)['temp'],
                           extrimely_cold)

        self.assertLess(get_weather("Riga", open_weather_token)['temp'],
                        get_weather("Dubai", open_weather_token)['temp'])

    def test_LanguagesCheck(self):
        """
        Проверяет корректность работы функции get_weather, если город
        введен на разных языках

        """

        self.assertSequenceEqual(get_weather("Riga", open_weather_token),
                                 get_weather("Rīga", open_weather_token),
                                 get_weather("Рига", open_weather_token))
        self.assertSequenceEqual(get_weather("pskov", open_weather_token),
                                 get_weather("псков", open_weather_token))

    def test_registersCheck(self):
        """
        Проверяет корректность работы функции get_weather,
        если город введен буквами разных регистров

        """

        self.assertEqual(get_weather("Riga", open_weather_token),
                         get_weather("РИГА", open_weather_token))

    def test_day_lengthCheck(self):
        """
        Проверяет корректность работы функции get_weather
        (длина дня совподает с временем заката минус время восхода)

        """

        self.assertEqual(get_weather("riga", open_weather_token)
                         ['sunset_timestamp'] -
                         get_weather("riga", open_weather_token)
                         ['sunrise_timestamp'],
                         get_weather("riga", open_weather_token)
                         ['length_of_the_day'])

    def test_typesCheck(self):
        """
        Проверяет корректность работы функции get_weather
        (что у данных правильный тип)

        """

        self.assertIsInstance(get_weather("ufa", open_weather_token)
                              ['city'], str)
        self.assertIsInstance(get_weather("riga", open_weather_token)
                              ['temp'], int)
        self.assertIsInstance(get_weather("омск", open_weather_token)
                              ['humidity'], int)
        self.assertIsInstance(get_weather("уфа", open_weather_token)
                              ['pressure'], int)
        self.assertIsInstance(get_weather("riga", open_weather_token)
                              ['wind'], float)
