import requests
from urllib.parse import urlparse


def get_comics_page_data(comics_id):
    comics_page_url = f'https://xkcd.com/{comics_id}/info.0.json'
    response = requests.get(comics_page_url)
    response.raise_for_status()
    return response.json()


def get_comics_filename(comics_page_data):
    comics_img_url = comics_page_data['img']
    return urlparse(comics_img_url).path[8:]


def get_author_comment(comics_page_data):
    return comics_page_data['alt']


def get_wall_upload_url(version, token, group_id):
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'v': version,
        'access_token': token,
        'group_id': group_id,
    }
    response = requests.get(url=url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def get_uploaded_img_dataset(upload_url, file_name):
    with open(f'{file_name}', 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def get_saved_to_album_photo_dataset(version, token, group_id, file_name):
    saved_photo_data = get_uploaded_img_dataset(get_wall_upload_url(version, token, group_id), file_name)
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'v': version,
        'access_token': token,
        'group_id': group_id,
        'photo': saved_photo_data['photo'],
        'server': saved_photo_data['server'],
        'hash': saved_photo_data['hash'],
    }
    response = requests.post(url=url, params=payload)
    response.raise_for_status()
    return response.json()['response'][0]

