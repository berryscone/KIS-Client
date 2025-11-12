import json
import os
import requests
from datetime import datetime
from typing import Tuple, Optional

from config import Config


# TODO: change log system to python built-in logging

TOKEN_FILE_NAME = "token.json"
KEY_ACCESS_TOKEN = "access_token"
KEY_ACCESS_TOKEN_EXPIRATION = "expired_at"


def convert_exp_time_str_to_datetime(exp_time_str):
    return datetime.strptime(exp_time_str, "%Y-%m-%d %H:%M:%S")


def load_token() -> Optional[Tuple[str, datetime]]:
    if not os.path.exists(TOKEN_FILE_NAME):
        return None

    result = None
    with open(TOKEN_FILE_NAME, "rt") as token_file:
        token_json = json.load(token_file)
        if KEY_ACCESS_TOKEN not in token_json or KEY_ACCESS_TOKEN_EXPIRATION not in token_json:
            return None

        access_token = token_json[KEY_ACCESS_TOKEN]
        expired_at_str = token_json[KEY_ACCESS_TOKEN_EXPIRATION]
        expired_at = convert_exp_time_str_to_datetime(expired_at_str)
        result = access_token, expired_at

    return result


def store_token(access_token: str, expired_at_str: str):
    with open(TOKEN_FILE_NAME, "wt") as token_file:
        token_dict = {
            "access_token": access_token,
            "expired_at": expired_at_str
        }
        token_file.write(json.dumps(token_dict))


def auth() -> Optional[Tuple[str, datetime]]:
    token_info = load_token()

    if token_info is None:
        cfg = Config()
        url_token = f"{cfg.BaseURL}/oauth2/tokenP"
        data = json.dumps(
            {
                "grant_type": "client_credentials",
                "appkey": cfg.AppKey,
                "appsecret": cfg.SecretKey,
            }
        )
        response = requests.post(url_token, data=data, headers=cfg.get_base_headers())
        if response.status_code != 200:
            print("Get Authentification token fail!\nYou have to restart your app!!!")
            return None

        response_json = response.json()
        access_token = response_json["access_token"]
        expired_at_str = response_json["access_token_token_expired"]
        expired_at = datetime.strptime(expired_at_str, "%Y-%m-%d %H:%M:%S")
        store_token(access_token, expired_at_str)
        token_info = access_token, expired_at

    return token_info
