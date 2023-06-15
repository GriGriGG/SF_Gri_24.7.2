import requests
from lib.logger import Logger

class MyRequests():

    '''Класс-обертка для выполнения HTTP-запросов'''

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, 'GET')

    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, 'POST')

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None):
        return MyRequests._send(url, data, headers, 'DELETE')


    @staticmethod
    def _send(url: str, data: dict, headers: dict, method: str):

        url = f'https://petfriends.skillfactory.ru{url}'

        if headers is None:
            headers = {}

        Logger.add_request(url, data, headers, method)


        if method == 'GET':
            response = requests.get(url, headers=headers, data=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, data=data)
        else:
            raise Exception(f"Использован неподходящий метод: '{method}'")

        Logger.add_response(response)

        return response