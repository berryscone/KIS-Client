import json
import requests
from datetime import datetime
from config import Config


def auth():
    cfg = Config()
    url_token = f"{cfg.BaseURL}/oauth2/tokenP"
    data = json.dumps(
        {
            "grant_type": "client_credentials",
            "appkey": cfg.AppKey,
            "appsecret": cfg.SecretKey,
        }
    )
    res = requests.post(url_token, data=data, headers=cfg.get_base_headers())
    rescode = res.status_code
    if rescode != 200:
        print("Get Authentification token fail!\nYou have to restart your app!!!")
        return None

    response_json = res.json()
    access_token = response_json["access_token"]
    expired_at_str = response_json["access_token_token_expired"]
    expired_at = datetime.strptime(expired_at_str, "%Y-%m-%d %H:%M:%S")

    return access_token, expired_at
