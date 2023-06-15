import json.decoder
from requests import Response
from datetime import datetime

class BaseCase:
    '''Базовый класс для тестовых случаев'''

    def get_json_value(self, response: Response, name):
        '''Метод для получения значения из JSON-ответа по ключу'''
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Пришёл ответ не в формате JSON. Текст ответа {response.text}"

        assert name in response_as_dict, f"JSON ответ не содержит ключ {name}"
        return response_as_dict[name]


    def get_key (self, response: Response, key):
        '''Метод для получения всего JSON-ответа'''
        assert key in response.json()
        return response.json()

    def get_header(self, response: Response, headers_name):
        '''Метод для получения значения заголовка ответа по его имени'''
        assert headers_name in response.headers
        return response.headers[headers_name]