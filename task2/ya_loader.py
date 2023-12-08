import requests
import urllib.request

API_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'


def get_real_direct_link(sharing_link: str) -> str:
    pk_request = requests.get(API_ENDPOINT.format(sharing_link))

    return pk_request.json()['href']