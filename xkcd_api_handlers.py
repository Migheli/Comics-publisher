import requests
import os
from urllib.parse import urlsplit, unquote


def get_comics_page_data(comics_id):
    comics_page_url = f'https://xkcd.com/{comics_id}/info.0.json'
    response = requests.get(comics_page_url)
    response.raise_for_status()
    return response.json()


def get_comics_filename(comics_img_url):
    url_path_unquoted = unquote(urlsplit(comics_img_url).path)
    filename = os.path.split(url_path_unquoted)[1]
    return filename


def get_author_comment(comics_page_data):
    return comics_page_data['alt']


def get_last_comics_id():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    response = response.json()
    return response['num']