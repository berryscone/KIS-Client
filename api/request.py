import requests

from config import Config


cfg = Config()


def get_request(api_url: str, headers: dict[str, str], params: dict[str, str]) -> requests.Response:
    url = f"{cfg.BaseURL}{api_url}"
    response = requests.get(url, headers=headers, params=params)
    return response
