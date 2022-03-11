import requests


def download_img(img_url, path_to_save):
    response = requests.get(img_url)
    response.raise_for_status()
    with open(path_to_save, 'wb') as file:
        file.write(response.content)

