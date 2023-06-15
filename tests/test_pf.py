from pet_friends_api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, invalid_key
import os
from dotenv import load_dotenv
load_dotenv()

from lib.assertions import Assertions
pf = PetFriends()
from lib.base_case import BaseCase


class TestsPetFriends(BaseCase):

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        """Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        response = pf.get_api_key(email, password)

        Assertions.assert_code_status(response.status_code, 200)
        Assertions.assert_json_has_key(response, 'key')

        auth_key = self.get_json_value(response, 'key')
        Assertions.assert_write_auth_key(auth_key)

    def test_get_all_pets_with_valid_key(self, filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        response = pf.get_api_key(valid_email, valid_password)
        key = self.get_json_value(response, 'key')
        status, result = pf.get_list_of_pets(key, filter)

        Assertions.assert_code_status(status, 200)
        assert len(result['pets']) > 0

    def test_get_my_pets_with_valid_key(self, filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        response = pf.get_api_key(valid_email, valid_password)
        key = self.get_json_value(response, 'key')
        status, result = pf.get_list_of_pets(key, filter)

        Assertions.assert_code_status(status, 200)
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_data(self, name='Мав', animal_type='Кiт',
                                         age='11', pet_photo='img/kit.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        Assertions.assert_code_status(status, 200)
        assert result['name'] == name


    def test_successful_update_self_pet_info(self, name='Шекель', animal_type='Пес', age=5):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            Assertions.assert_code_status(status, 200)
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")


    def test_successful_delete_self_pet(self):
        """Проверяем возможность удаления питомца"""
        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(auth_key, "Маф", "Кiт", "12", 'img/kit.jpg')
            _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        Assertions.assert_code_status(status, 200)
        assert pet_id not in my_pets.values()





        """"Далее идет код написаный для задания 24.7.2"""





        # Проверка на создание питомца "простым методом без фото"
    def test_add_new_pet_simple(self, name='Мав', animal_type='Кiт',
                                         age='4'):

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_nofoto(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        Assertions.assert_code_status(status, 200)
        assert result['name'] == name


        # Проверка на добавление фото к существующему питомцу
    def test_add_photo(self, pet_photo='img/kit.jpg'):

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            Assertions.assert_code_status(status, 200)
            assert result['pet_photo']
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")


    # Проверка на пустые значения в Логине и Пароле
    def test_get_api_key_for_user_empty(self, email="_", password="_"):

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        Assertions.assert_code_status(status, 403)
        assert 'key' not in result

    # Проверка на неправильный пароль
    def test_get_api_key_for_invalid_password(self, email=valid_email, password=invalid_password):

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        Assertions.assert_code_status(status, 403)
        assert 'key' not in result
        print("\nСтатус: ", status)
        print(result)


    def test_get_api_key_for_invalid_email(self, email=invalid_email, password=valid_password):

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        Assertions.assert_code_status(status, 403)
        assert 'key' not in result
        print("\nСтатус: ", status)
        print(result)


        # Проверка того, что запрос списка всех питомцев c некорректным значением API-ключа возвращает статус 403
    def test_get_all_pets_with_invalid_key(self, filter=''):

        auth_key = invalid_key
        status, result = pf.get_list_of_pets(auth_key, filter)

        Assertions.assert_code_status(status, 403)


        """Тесты на некорректное поведение системы (баги). Для ассерта выполнен код 400, как ожидаемый, 
        но по факту всё работает с кодом 200"""


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

