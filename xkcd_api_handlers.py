import requests
from urllib.parse import urlparse
from img_downloader import download_img


def save_comics_to_file(comics_page_data):
    comics_img_url = comics_page_data['img']
    download_img(comics_img_url, get_comics_filename(comics_page_data))


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


def get_last_comics_id():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    response = response.json()
    return response['num']