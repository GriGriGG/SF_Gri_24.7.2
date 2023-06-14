import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    def test_setup(self):
        headers = {
            'email': 'shalom_dude@gmail.com',
            'password': 'qwerty'
        }
        response1 = requests.get('https://petfriends.skillfactory.ru/api/key', headers=headers)

        assert response1.status_code == 200
        req_json = response1.json()
        assert "key" in req_json

        key_value = req_json['key']
        print(key_value)

    def test_auth_user(self):
        headers = {
            'email': 'shalom_dude@gmail.com',
            'password': 'qwerty'
        }
        response2 = requests.get('https://petfriends.skillfactory.ru/api/key', headers=headers)

        # Assertions.assert_json_value_by_name(
        #     response2,
        #     'key',
        #     self.get_json_value(response2, 'key')
        # )
