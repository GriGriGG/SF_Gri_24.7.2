from pet_friends_api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, invalid_key
import os
from dotenv import load_dotenv

load_dotenv()
from lib.my_requests import MyRequests
from lib.assertions import Assertions

pf = PetFriends()
from lib.base_case import BaseCase
import json


class TestsPetFriends(BaseCase):
    def setup(self):
        headers = {
            'email': 'shalom_dude@gmail.com',
            'password': 'qwerty'
        }
        response = MyRequests.get('/api/key', headers=headers)
        self.headers = self.get_header(response, 'Content-Type')
        self.auth_key = self.get_json_value(response, 'key')
        BaseCase.update_auth_key(self.auth_key)

    def test_get_api_key_for_valid_user(self):
        """Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
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
        """ Проверяем что запрос всех питомцев возвращает не пустой список."""

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
        Assertions.assert_code_status(response, 200)

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

    # def test_get_api_key_for_user_empty(self, email="shalom_dude@gmail.com", password="_"):
    #
    #     headers = {
    #         'email': email,
    #         'password': password
    #     }
    #     response = MyRequests.get('/api/key', headers=headers)
    #
    #     Assertions.assert_list_not_empty(response)



    # # Проверка на неправильный пароль
    # def test_get_api_key_for_invalid_password(self, email=valid_email, password=invalid_password):
    #
    #     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    #     status, result = pf.get_api_key(email, password)
    #
    #     # Сверяем полученные данные с нашими ожиданиями
    #     Assertions.assert_code_status(status, 403)
    #     assert 'key' not in result
    #     print("\nСтатус: ", status)
    #     print(result)
    #
    # def test_get_api_key_for_invalid_email(self, email=invalid_email, password=valid_password):
    #
    #     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    #     status, result = pf.get_api_key(email, password)
    #
    #     # Сверяем полученные данные с нашими ожиданиями
    #     Assertions.assert_code_status(status, 403)
    #     assert 'key' not in result
    #     print("\nСтатус: ", status)
    #     print(result)

        # Проверка того, что запрос списка всех питомцев c некорректным значением API-ключа возвращает статус 403

    def test_get_all_pets_with_invalid_key(self):

        headers = {
            'auth_key': '111aaaaaa111aa1111a1111111111aaaa1111111111111aaaa111111'
            # 'auth_key': self.auth_key
        }
        response = MyRequests.get('/api/pets', headers=headers)
        response = MyRequests.get('/api/pets', headers=headers)
        self.assertEqual(response.status_code, 403, "Статус ответа не равен 403")
        Assertions.assert_code_status(response.status_code, 200)
        # BaseCase.get_response_data(response.headers, 200)
        # Assertions.assert_json_key_in_response(response, "pets")

# """Тесты на некорректное поведение системы (баги). Для ассерта выполнен код 400, как ожидаемый,
# но по факту всё работает с кодом 200"""

        # Проверка на создание питомца с пустыми значением имени

    def test_add_new_pet_simple_without_name(self, name='', animal_type='Котопёс',
                                             age='2'):

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_nofoto(auth_key, name, animal_type, age)

        Assertions.assert_code_status(status, 400)

        # Проверка на создание питомца с пустыми значением породы

    def test_add_new_pet_simple_without_animal_type(self, name='Котофея', animal_type='',
                                                    age='2'):

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_nofoto(auth_key, name, animal_type, age)

        Assertions.assert_code_status(status, 400)

        # Проверка на создание питомца с пустыми значением возраста

    def test_add_new_pet_simple_without_age(self, name='Котофеша', animal_type='Кошечка',
                                            age=''):

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_nofoto(auth_key, name, animal_type, age)

        Assertions.assert_code_status(status, 400)

        # Проверка на создание питомца с пустыми значением во всех полях ввода

    def test_add_new_pet_simple_without_all(self, name='', animal_type='',
                                            age=''):

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_nofoto(auth_key, name, animal_type, age)

        Assertions.assert_code_status(status, 400)
