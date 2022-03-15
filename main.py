import os
import traceback
from environs import Env
from random import randint
from img_downloader import download_img
from vk_api_handlers import get_saved_to_album_photo_dataset, post_on_wall, VkApiError
from xkcd_api_handlers import get_comics_page_data, get_comics_filename, get_last_comics_id


def main():

    env = Env()
    env.read_env()
    version = env('VERSION')
    token = env('VK_ACCESS_TOKEN')
    group_id = env('GROUP_ID')
    first_comics_id, last_comics_id = 1, get_last_comics_id()
    comics_id = randint(first_comics_id, last_comics_id)
    comics_page_data = get_comics_page_data(comics_id)
    comics_img_url, auhtor_comment = comics_page_data['img'], comics_page_data['alt']
    download_img(comics_img_url, get_comics_filename(comics_img_url))
    file_name = get_comics_filename(comics_img_url)
    try:
        saved_photo_dataset = get_saved_to_album_photo_dataset(version, token, group_id, file_name)
        post_on_wall(version, 'token', group_id, saved_photo_dataset, auhtor_comment)
    except VkApiError:
        exit(f'{traceback.format_exc()}')
    finally:
        os.remove(file_name)


if __name__ == '__main__':
    main()