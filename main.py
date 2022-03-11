import requests
import os
from environs import Env
from random import randint
from img_downloader import download_img
from getters import get_comics_page_data, get_comics_filename, get_author_comment, get_saved_to_album_photo_dataset


def save_comics_to_file(comics_page_data):
    comics_img_url = comics_page_data['img']
    download_img(comics_img_url, get_comics_filename(comics_page_data))


def post_on_wall(version, token, group_id, saved_photo_dataset, comment):
    url = f'https://api.vk.com/method/wall.post?PARAMS'
    payload = {
        'v': version,
        'access_token': token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': comment,
        'attachments': f'photo{saved_photo_dataset["owner_id"]}_{saved_photo_dataset["id"]}'
    }

    response = requests.post(url=url, params=payload)
    response.raise_for_status()
    reponse_data = response.json()['response']
    return reponse_data


def main():

    env = Env()
    env.read_env()
    version = env('VERSION')
    token = env('VK_ACCESS_TOKEN')
    group_id = env('GROUP_ID')
    first_comics_id, last_comics_id = 1, 2591
    comics_id = randint(first_comics_id, last_comics_id)
    comics_page_data = get_comics_page_data(comics_id)
    save_comics_to_file(comics_page_data)
    file_name = get_comics_filename(comics_page_data)
    saved_photo_dataset = get_saved_to_album_photo_dataset(version, token, group_id, file_name)
    post_on_wall(version, token, group_id, saved_photo_dataset, get_author_comment(comics_page_data))
    os.remove(file_name)


if __name__ == '__main__':
    main()