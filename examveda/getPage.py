
import requests


def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None