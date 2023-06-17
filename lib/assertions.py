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

    # @staticmethod
    # def assert_json_value_by_name(response:Response, name, expected_value, error_message):
    #     try:
    #         response_as_dict = response.json()
    #     except json.JSONDecodeError:
    #         assert False, f"Ответ не в формате JSON. Текст ответа '{response.text}'"
    #
    #     assert name in response_as_dict, f"JSON ответ не содержит {name}"
    #     assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_key_in_response(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа '{response.text}'"

        if key in response_as_dict:
            print(f"Ключ '{key}' найден в теле ответа")
        else:
            print(f"Ключ '{key}' не найден в теле ответа")

    @staticmethod
    def assert_json_value_by_name(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в формате JSON. Текст ответа '{response.text}'"

        if name in response_as_dict.values():
            print(f"Значение '{name}' найдено в теле ответа")
        else:
            print(f"Значение '{name}' не найдено в теле ответа")

    @staticmethod
    def assert_list_not_empty(lst, error_message):
        assert len(lst) > 0, error_message

    # @staticmethod
    # def assert_json_has_key(response: Response, key):
    #     '''Утверждение: JSON-ответ содержит указанный ключ'''
    #     try:
    #         response_as_dict = response.json()
    #     except json.JSONDecodeError:
    #         assert False, f"Пришёл ответ не в формате JSON. Текст ответа '{response.text}'"
    #
    #     assert key in response_as_dict, f"JSON ответ не содержит ключ '{key}'"
    # @staticmethod
    # def assert_json_has_key(response: dict, key):
    #     '''Утверждение: JSON-ответ содержит указанный ключ'''
    #     assert key in response, f"JSON-ответ не содержит ключ '{key}'"

    @staticmethod
    def assert_code_status(status: int, expected_status_code):
        '''Утверждение: статус код ответа соответствует ожидаемому'''
        assert status == expected_status_code, \
            f"Непредсказуемый статус код! Ожидаемый: {expected_status_code}. Полученный: {status}"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        '''Утверждение: JSON-ответ не содержит указанный ключ'''
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Пришёл ответ не в формате JSON. Текст ответа '{response.text}'"

        assert name not in response_as_dict, f"JSON ответ не содержит ключ '{name}'"

    # @staticmethod
    # def assert_update_pet_id(new_value):
    #     config = configparser.ConfigParser()
    #     config.read('../.env')
    #     if 'DEFAULT' not in config:
    #         config['DEFAULT'] = {}
    #     config.set('DEFAULT', 'new_pet_id', new_value)
    #     with open('../.env', 'w') as f:
    #         config.write(f)
    #     os.environ['new_pet_id'] = new_value
    #
    # @staticmethod
    # def assert_write_pet_name(new_value):
    #     config = configparser.ConfigParser()
    #     config.read('../.env')
    #     if 'DEFAULT' not in config:
    #         config['DEFAULT'] = {}
    #     config.set('DEFAULT', 'name', new_value)
    #     with open('../.env', 'w') as f:
    #         config.write(f)
    #     os.environ['name'] = new_value

    # @staticmethod
    # def assert_write_auth_key(new_value):
    #     config = configparser.ConfigParser()
    #     config.read('../.env')
    #     if 'DEFAULT' not in config:
    #         config['DEFAULT'] = {}
    #     config.set('DEFAULT', 'auth_key', new_value)
    #     with open('../.env', 'w') as f:
    #         config.write(f)
    #     os.environ['auth_key'] = new_value

    @staticmethod
    def assert_not_empty_response(response):
        """Утверждение: ответ от сервера является пустым"""
        assert len(response) > 0, "Ответ от сервера не является пустым"

    @staticmethod
    def check_response_type(url):
        response = requests.get(url)

        # Получаем заголовок Content-Type из ответа
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            print('Ответ сервера содержит JSON')
            try:
                json_data = response.json()
                print('JSON данные:', json_data)
            except ValueError:
                print('Ошибка декодирования JSON')
                assert False, 'Ошибка декодирования JSON'
        elif 'text/html' in content_type:
            print('Ответ сервера содержит HTML')
            html_data = response.text
            print('HTML данные:', html_data)
        else:
            print('Ответ сервера содержит другой тип данных:', content_type)
            assert False, 'Ответ сервера содержит другой тип данных'

