import datetime
import os
import json

from requests import Response

class Logger:
    '''Cоздание лога в директории "logs"'''
    log_dir = os.path.abspath("../logs")
    file_name = os.path.join(log_dir, f"log_{datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log")

    @classmethod
    def _write_log_to_file(cls, data: str):
        if not os.path.exists(cls.log_dir):
            os.makedirs(cls.log_dir)
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url:str, data: dict, headers: dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f'\n--REQUESTS--\n'
        data_to_add += f'Test: {testname}\n'
        data_to_add += f'Time: {str(datetime.datetime.now())}\n'
        data_to_add += f'Request method: {method}\n'
        data_to_add += f'Request URL: {url}\n'
        data_to_add += f'Request headers: {json.dumps(headers, indent=4)}\n'
        data_to_add += f'Request data: {json.dumps(data, indent=4)}\n'

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        headers_as_dict = dict(response.headers)
        response_text = json.dumps(response.json(), indent=4)  # Преобразование словаря в JSON-строку с отступами
        response_text = response_text.replace('\\"', '"')  # Удаление экранирования символов обратной косой черты

        data_to_add = f'\n--RESPONSE--\n'
        data_to_add += f'Response code: {response.status_code}\n'
        data_to_add += f'Response header: {json.dumps(headers_as_dict, indent=4)}\n'
        data_to_add += f'Response text: {response_text}\n'  # Добавление двойных кавычек в начало и конец строки
        data_to_add += f'\n-----\n'

        cls._write_log_to_file(data_to_add)
