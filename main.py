import os
from environs import Env
from random import randint
from vk_api_handlers import get_saved_to_album_photo_dataset, post_on_wall
from xkcd_api_handlers import save_comics_to_file, get_comics_page_data, get_comics_filename, \
    get_author_comment, get_last_comics_id


def main():

    env = Env()
    env.read_env()
    version = env('VERSION')
    token = env('VK_ACCESS_TOKEN')
    group_id = env('GROUP_ID')
    first_comics_id, last_comics_id = 1, get_last_comics_id()
    comics_id = randint(first_comics_id, last_comics_id)
    comics_page_data = get_comics_page_data(comics_id)
    save_comics_to_file(comics_page_data)
    file_name = get_comics_filename(comics_page_data)
    saved_photo_dataset = get_saved_to_album_photo_dataset(version, token, group_id, file_name)
    post_on_wall(version, token, group_id, saved_photo_dataset, get_author_comment(comics_page_data))
    os.remove(file_name)


if __name__ == '__main__':
    main()