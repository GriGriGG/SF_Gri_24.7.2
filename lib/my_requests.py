import requests
from lib.logger import Logger


class MyRequests():
    """Класс-обертка для выполнения HTTP-запросов"""

    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None):
        return MyRequests._send(url, params=params, headers=headers, method='GET')

    @staticmethod
    def post(url: str, data: dict = None, files: dict = None, headers: dict = None):
        return MyRequests._send(url, data=data, files=files, headers=headers, method='POST')

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None):
        return MyRequests._send(url, data=data, headers=headers, method='PUT')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None):
        return MyRequests._send(url, data=data, headers=headers, method='DELETE')

    @staticmethod
    def _send(url: str,
              params: dict = None,
              files: dict = None,
              data: dict = None,
              headers: dict = None,
              method: str = 'GET'):
        url = f'https://petfriends.skillfactory.ru{url}'

        if headers is None:
            headers = {}
        if data is None:
            data = {}

        Logger.add_request(url, data, headers, method)

        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, data=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data, files=files)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, data=data)
        else:
            raise Exception(f"Использован неподходящий метод: '{method}'")

        Logger.add_response(response)

        return response
