import os
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
from datetime import datetime
from dotenv import load_dotenv
from io import open
load_dotenv()
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class TestPetFriends(BaseCase):
    def setup(self):
        headers = {
            'email': 'shalom_dude@gmail.com',
            'password': 'qwerty'
        }
        response = MyRequests.get('/api/key', headers=headers)

        # получение auth_key
        req_json = response.json()
        assert "key" in req_json
        self.auth_key = req_json['key']

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'key')


        random_part = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

        self.name_pet = f"Kit{random_part}"
        self.animal_type_pet = "Cat"
        self.age_pet = "1"

        self.new_pet_id = os.getenv('new_pet_id')

    def test_created_pet(self):
        # CREATE
        headers = {
            'auth_key': self.auth_key,
        }
        data = {
            'name': self.name_pet,
            'animal_type': self.animal_type_pet,
            'age': self.age_pet,
        }
        response = MyRequests.post('/api/create_pet_simple', headers=headers, data=data)
        response_text = response.content.decode("utf-8")

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "name")
        Assertions.assert_json_has_key(response, "id")

        self.pet_id = response.json()["id"]
        self.pet_name = response.json()['name']
        Assertions.assert_update_pet_id(self.pet_id)
        Assertions.assert_write_pet_name(self.pet_name)

    def test_get_the_list_of_pets(self):
        # GET_THE_LIST_OF_PETS
        headers = {
            'auth_key': self.auth_key
        }

        response = MyRequests.get('/api/pets?filter=my_pets', headers=headers)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "pets")

    def test_edit_last_pet(self):
        # EDIT_PETS
        headers = {
            'auth_key': self.auth_key,
        }
        data = {
            'name': "Changed_name",
            'animal_type': self.animal_type_pet,
            'age': self.age_pet,
            'pet_photo': ''
        }
        response = MyRequests.put(f'/api/pets/{self.new_pet_id}', headers=headers, data=data)

        Assertions.assert_code_status(response, 200)

    def test_add_photo(self, pet_photo='img/kit.jpg'):
        # ADD_PHOTO_OF_PET
        # data = {
        #     'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        # }

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {
            'auth_key': self.auth_key,
            'Content-Type': data.content_type
        }

        url = f'https://petfriends.skillfactory.ru/api/pets/set_photo/{self.new_pet_id}'
        response = MyRequests.post(url, headers=headers, data=data)
        # response = MyRequests.post(f'/api/pets/set_photo/{self.new_pet_id}', headers=headers, data=data)
        Assertions.assert_json_has_key(response, 'age')
        Assertions.assert_code_status(response, 200)

        # status = response.status_code
        # try:
        #     result = response.json()
        # except json.decoder.JSONDecodeError:
        #     result = response.text
        # print(result)
        # return status, result



    def test_emoving_all_values_via_an_empty_query(self):
        # _PETS
        headers = {
            'auth_key': self.auth_key,
        }

        response = MyRequests.put(f'/api/pets/{self.new_pet_id}', headers=headers)

        Assertions.assert_code_status(response, 200)

    def test_delete_last_pet(self):
        # DELETE_PETS
        headers = {
            'auth_key': self.auth_key,
        }

        response = MyRequests.delete(f'/api/pets/{self.new_pet_id}', headers=headers)

        Assertions.assert_code_status(response, 200)

        # status = response.status_code
        # try:
        #     result = response.json()
        # except json.decoder.JSONDecodeError:
        #     result = response.text
        # print(result)
        # return status, result
