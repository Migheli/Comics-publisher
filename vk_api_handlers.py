import requests


def get_wall_upload_url(version, token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'v': version,
        'access_token': token,
        'group_id': group_id,
    }
    response = requests.get(url=url, params=payload)
    response.raise_for_status()
    response_data = response.json()
    is_valid_vk_response(response_data)
    return response_data['response']['upload_url']


def get_uploaded_img_dataset(upload_url, file_name):
    with open(f'{file_name}', 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        response_data = response.json()
        is_valid_vk_response(response_data)
        return response_data


def get_saved_to_album_photo_dataset(version, token, group_id, file_name):
    saved_photo_data = get_uploaded_img_dataset(get_wall_upload_url(version, token, group_id), file_name)
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
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
    response_data = response.json()
    is_valid_vk_response(response_data)
    return response_data['response'][0]


def post_on_wall(version, token, group_id, saved_photo_dataset, comment):
    url = 'https://api.vk.com/method/wall.post'
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
    response_data = response.json()
    is_valid_vk_response(response_data)
    return response_data['response']


class VkApiError(Exception):
    pass


def is_valid_vk_response(response_data):
    if 'error' in response_data:
        error = response_data['error']
        error_code, error_description = error['error_code'], error['error_msg']
        raise VkApiError(f'VK API ERROR. Code: {error_code} Description: {error_description}')
    else:
        pass

