from requests import Response
import json
import configparser
import os
import requests


class Assertions:
    """Готовые наборы команд для ускорения написания тестов:
    проверка статус кода,
    нахождение в ответе ключевых слов,
    запись строк в файл .env"""

    @staticmethod
    def assert_json_key_in_response(response: Response, key):
        """Утверждение: JSON-ответ содержит указанный ключ"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа '{response.text}'"

        if key in response_as_dict:
            print(f"Ключ '{key}' найден в теле ответа")
        else:
            print(f"Ключ '{key}' не найден в теле ответа")

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        """Утверждение: JSON-ответ не содержит указанный ключ"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Пришёл ответ не в формате JSON. Текст ответа '{response.text}'"

        assert name not in response_as_dict, f"JSON ответ не содержит ключ '{name}'"

    @staticmethod
    def assert_json_value_by_name(response: Response, name):
        """Утверждение: JSON-ответ содержит указанное значение"""
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа '{response.text}'"

        if name in response_as_dict.values():
            print(f"Значение '{name}' найдено в теле ответа")
        else:
            print(f"Значение '{name}' не найдено в теле ответа")

    @staticmethod
    def assert_code_status(status: int, expected_status_code):
        """Утверждение: статус код ответа соответствует ожидаемому"""
        assert status == expected_status_code, \
            f"Непредсказуемый статус код! Ожидаемый: {expected_status_code}. Полученный: {status}"

    # @staticmethod
    # def assert_json_value_by_name(response:Response, name, expected_value, error_message):
    #     try:
    #         response_as_dict = response.json()
    #     except json.JSONDecodeError:
    #         assert False, f"Ответ не в формате JSON. Текст ответа '{response.text}'"
    #
    #     assert name in response_as_dict, f"JSON ответ не содержит {name}"
    #     assert response_as_dict[name] == expected_value, error_message
