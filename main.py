import json

from config import Config
from api.auth import auth
from api.price import get_price
from api.account import get_oversee_balance, get_account_balance


def dump_json_dict(json_dict: dict):
    return json.dumps(json_dict, indent=2, ensure_ascii=False)


cfg = Config()
access_token, access_token_expired_at = auth()
apple_price = get_price(access_token, "NAS", "AAPL")
print(dump_json_dict(apple_price))

oversee_balance = get_oversee_balance(access_token, "NASD", "USD")
print(dump_json_dict(oversee_balance))

account_balance = get_account_balance(access_token)
print(account_balance)
