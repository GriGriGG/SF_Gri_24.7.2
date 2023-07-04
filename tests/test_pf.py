import os
from dotenv import load_dotenv
from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import json
load_dotenv()

class TestsPetFriends(BaseCase):
    def setup(self):
        """Первый запрос на получение ключа аутентификации и запись значения в .env"""
        headers = {
            'email': 'shalom_dude@gmail.com',
            'password': 'qwerty'
        }
        response = MyRequests.get('/api/key', headers=headers)
        self.headers = self.get_header(response, 'Content-Type')
        self.auth_key = self.get_json_value(response, 'key')
        BaseCase.update_auth_key(self.auth_key)

    def test_get_api_key_for_valid_user(self):
        """Проверяем что запрос api ключа возвращает статус 200 и в результате содержится key"""
        headers = {
            'email': 'shalom_dude@gmail.com',
            'password': 'qwerty'
        }
        response = MyRequests.get('/api/key', headers=headers)
        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_key_in_response(response, 'key')

    def test_get_all_pets_with_valid_key(self):
        """ Проверяем что запрос всех питомцев возвращает не пустой список."""
        headers = {
            'auth_key': self.auth_key
        }
        response = MyRequests.get('/api/pets', headers=headers)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_key_in_response(response, "pets")
        # assert len(response3['pets']) > 0

    def test_get_my_pets_with_valid_key(self):
        """ Проверяем что запрос питомцев пользователя возвращает не пустой список."""
        headers = {
            'auth_key': self.auth_key
        }
        response = MyRequests.get('/api/pets?filter=', headers=headers)

        Assertions.assert_code_status(response.status_code, 200)

        response_json = response.text
        response_data = json.loads(response_json)
        Assertions.assert_json_key_in_response(response, "pets")
        Assertions.assert_list_not_empty(response_data['pets'], 'Список питомцев пуст')

    def test_add_new_pet_with_valid_data(self, name='Йцукен', animal_type='Пеленг', age='11', pet_photo='img/p.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        files = {'pet_photo': open(pet_photo, 'rb')}
        response = MyRequests.post('/api/pets', headers=headers, data=data, files=files)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_value_by_name(response, name)

        pet_id = self.get_json_value(response, 'id')
        BaseCase.update_pet_id(pet_id)

    def test_successful_update_self_pet_info(self, name='Цац Илкаш', animal_type='Пеленг', age=5):
        """Проверяем возможность обновления информации о питомце"""
        pet_id = os.getenv('NEW_PET_ID')
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = MyRequests.put(f'/api/pets/{pet_id}', headers=headers, data=data)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_value_by_name(response, name)

    def test_delete(self):
        """Проверяем возможность удаления питомца"""
        pet_id = os.getenv('NEW_PET_ID')
        headers = {
            'auth_key': self.auth_key
        }
        response = MyRequests.delete(f'/api/pets/{pet_id}', headers=headers)

        # БАГ нет ответа от сервера
        Assertions.assert_code_status(response.status_code, 200)

    def test_add_new_pet_simple(self, name='Тардым Бабах', animal_type='Малок', age='22'):
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = MyRequests.post('/api/create_pet_simple', headers=headers, data=data)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_value_by_name(response, name)

        pet_id_simple = self.get_json_value(response, 'id')
        BaseCase.update_pet_id_simple(pet_id_simple)

    def test_add_photo(self, pet_photo='img/m.jpg'):
        pet_id = os.getenv('NEW_PET_ID_SIMPLE')
        headers = {
            'auth_key': self.auth_key
        }

        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        files = {'pet_photo': open(pet_photo, 'rb')}

        response = MyRequests.post(f'/api/pets/set_photo/{pet_id}', headers=headers, files=files)
        Assertions.assert_code_status(response.status_code, 200)

    def test_add_new_pet_simple_without_name(self, name='', animal_type='Клисан', age='2'):
        """Питомец без имени"""
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = MyRequests.post('/api/create_pet_simple', headers=headers, data=data)

        Assertions.assert_code_status(response.status_code, 200)

    def test_add_new_pet_simple_without_animal_type(self, name='Пенчекряк', animal_type='', age='1'):
        """Питомец без типа"""
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = MyRequests.post('/api/create_pet_simple', headers=headers, data=data)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_value_by_name(response, name)

        pet_id_simple = self.get_json_value(response, 'id')
        BaseCase.update_pet_id_simple(pet_id_simple)

    def test_add_new_pet_simple_without_age(self, name='Рачехан', animal_type='Человек', age=''):
        """Питомец без возраста"""
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = MyRequests.post('/api/create_pet_simple', headers=headers, data=data)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_value_by_name(response, name)

        pet_id_simple = self.get_json_value(response, 'id')
        BaseCase.update_pet_id_simple(pet_id_simple)

    def test_add_new_pet_simple_without_all(self, name='', animal_type='', age=''):
        """Питомец без параметров"""
        headers = {
            'auth_key': self.auth_key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        response = MyRequests.post('/api/create_pet_simple', headers=headers, data=data)

        Assertions.assert_code_status(response.status_code, 200)

        pet_id_simple = self.get_json_value(response, 'id')
        BaseCase.update_pet_id_simple(pet_id_simple)