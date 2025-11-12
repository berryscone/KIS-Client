from config import Config
from api.request import get_request


cfg = Config()


def get_price(access_token: str, excd: str, symbol: str):
    headers = cfg.get_base_headers()
    headers["authorization"] = f"Bearer {access_token}"
    headers["appkey"] = cfg.AppKey
    headers["appsecret"] = cfg.SecretKey
    headers["tr_id"] = "HHDFS00000300"

    params = {
        "AUTH": "",
        "EXCD": excd,
        "SYMB": symbol,
    }

    res = get_request(
        api_url="/uapi/overseas-price/v1/quotations/price",
        headers=headers,
        params=params,
    )
    if res.status_code != 200:
        print(f"error - {res.json()}")

    res_json = res.json()
    return res_json
