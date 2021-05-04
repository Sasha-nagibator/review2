import unittest
from main import get_weather
from config import open_weather_token


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

        self.assertGreater(get_weather("Riga", open_weather_token)[1], -50)

        self.assertLess(get_weather("Riga", open_weather_token)[1],
                        get_weather("Dubai", open_weather_token)[1])

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

        self.assertEqual(get_weather("ош", open_weather_token)[6] -
                         get_weather("ош", open_weather_token)[5],
                         get_weather("ош", open_weather_token)[7])

    def test_typesCheck(self):
        """
        Проверяет корректность работы функции get_weather
        (что у данных правильный тип)

        """

        self.assertIsInstance(get_weather("ufa", open_weather_token)[0], str)
        self.assertIsInstance(get_weather("riga", open_weather_token)[1], int)
        self.assertIsInstance(get_weather("омск", open_weather_token)[2], int)
        self.assertIsInstance(get_weather("уфа", open_weather_token)[3], int)
        self.assertIsInstance(get_weather("riga", open_weather_token)[4],
                              float)
