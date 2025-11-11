import json
import copy
import requests
from config import Config
from auth import auth

cfg = Config()
access_token, access_token_expired_at = auth()
tr_id = "HHDFS00000300"
url = f"{cfg.BaseURL}/uapi/overseas-price/v1/quotations/price"
params = {
    "AUTH": "",
    "EXCD": "NAS",
    "SYMB": "AAPL",
}

headers = cfg.get_base_headers()
headers["authorization"] = f"Bearer {access_token}"
headers["appkey"] = cfg.AppKey
headers["appsecret"] = cfg.SecretKey
headers["tr_id"] = tr_id

res = requests.get(url, headers=headers, params=params)
if res.status_code != 200:
    print(f"error - {res.json()}")

res_json = res.json()
