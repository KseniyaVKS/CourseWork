import time
from tqdm import tqdm
import requests
import json
from pprint import pprint

with open('token_vk.txt', 'r') as f:
    token_vk = f.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, vk_id, count=5):
        """Метод получения фотографий с профиля"""
        photo_url = self.url + 'photos.get'
        params = {
            'owner_id': vk_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
        }
        req = requests.get(photo_url, params={**self.params, **params}).json()
        data_photos_list = req['response']['items']
        photos_dict = {}
        for photo in tqdm(data_photos_list[:count]):
            time.sleep(0.1)
            name_photo = photo['likes']['count']
            date_photo = photo['date']

            type_list = []
            for size in tqdm(photo['sizes']):
                time.sleep(0.1)
                type_list.append(size['type'])
            sorted(type_list, key=lambda x: 'w')

            if size['type'] == type_list[-1]:
                url_photo = size['url']
                type_size = size['type']

            if name_photo in photos_dict:
                name_photo = str(name_photo) + '_' + str(date_photo)
                photos_dict[name_photo] = [url_photo, type_size]
            else:
                photos_dict[name_photo] = [url_photo, type_size]
        return photos_dict


class YandexDisk:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            "Authorization": self.token
        }

    def folder(self):
        """Метод создает папку с именем 'for_coursework' на Яндекс Диске"""
        url = self.url
        params = {
            "path": 'for_coursework'
        }
        headers = self.get_headers()
        res = requests.put(url, headers=headers, params=params)
        if res.status_code == 409:
            pass

    def upload(self):
        """Метод загружает файл на Яндекс Диск"""
        photos_dict = vk_client.get_photos(vk_id)
        list_for_json_file = []
        for name_photo, info_photo in tqdm(photos_dict.items()):
            time.sleep(0.1)
            name = str(name_photo) + '.jpg'
            list_for_json_file.append({"file_name": name, "size": info_photo[1]})
            url_upload = self.url + 'upload'
            params = {
                "path": 'for_coursework/' + name,
                "url": info_photo[0]
            }
            headers = self.get_headers()
            res = requests.post(url_upload, headers=headers, params=params)
        return list_for_json_file


def json_file():
    """Функция записывает информацию о фото в json-файл"""
    list_for_json_file = YandexDisk.upload()
    with open("info_photos.json", "w") as f:
        json.dump(list_for_json_file, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    vk_id = input("Введите id пользователя vk: ")
    token = input("Введите токен Яндекса: ")
    YandexDisk = YandexDisk(token)
    YandexDisk.folder()
    vk_client = VkUser(token_vk, '5.131')
    json_file()
