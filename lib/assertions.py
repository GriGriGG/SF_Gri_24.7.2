from requests import Response
import json
import configparser
import os


class Assertions:

    """Готовые наборы команд для ускорения написания тестов:
    проверка статус кода,
    нахождение в ответе ключевых слов,
    запись строк в файл .env"""

    @staticmethod
    def assert_json_has_key(response: Response, key):
        '''Утверждение: JSON-ответ содержит указанный ключ'''
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Пришёл ответ не в формате JSON. Текст ответа '{response.text}'"

        assert key in response_as_dict, f"JSON ответ не содержит ключ '{key}'"

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

    @staticmethod
    def assert_update_pet_id(new_value):
        config = configparser.ConfigParser()
        config.read('../.env')
        if 'DEFAULT' not in config:
            config['DEFAULT'] = {}
        config.set('DEFAULT', 'new_pet_id', new_value)
        with open('../.env', 'w') as f:
            config.write(f)
        os.environ['new_pet_id'] = new_value

    @staticmethod
    def assert_write_pet_name(new_value):
        config = configparser.ConfigParser()
        config.read('../.env')
        if 'DEFAULT' not in config:
            config['DEFAULT'] = {}
        config.set('DEFAULT', 'name', new_value)
        with open('../.env', 'w') as f:
            config.write(f)
        os.environ['name'] = new_value

    @staticmethod
    def assert_write_auth_key(new_value):
        config = configparser.ConfigParser()
        config.read('../.env')
        if 'DEFAULT' not in config:
            config['DEFAULT'] = {}
        config.set('DEFAULT', 'auth_key', new_value)
        with open('../.env', 'w') as f:
            config.write(f)
        os.environ['auth_key'] = new_value

