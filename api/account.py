from typing import List
from dataclasses import dataclass, fields

from wcwidth import wcswidth

from config import Config
from api.request import get_request


def align_left(text, width):
    pad = width - wcswidth(text)
    return text + " " * pad


@dataclass
class AccountBalance:
    pchs_amt: float
    evlu_amt: float
    evlu_pfls_amt: float
    crdt_lnd_amt: float
    real_nass_amt: float
    whol_weit_rt: float

    def __post_init__(self):
        for f in fields(self):
            if f.type == float:
                val = getattr(self, f.name)
                setattr(self, f.name, float(val))

    def __str__(self):
        return (
            f"  {align_left("매입 금액", 15)}: {self.pchs_amt:,.0f}\n"
            f"  {align_left("평가 금액", 15)}: {self.evlu_amt:,.0f}\n"
            f"  {align_left("평가 손익 금액", 15)}: {self.evlu_pfls_amt:,.0f}\n"
            f"  {align_left("신용 대출 금액", 15)}: {self.crdt_lnd_amt:,.0f} \n"
            f"  {align_left("순자산 금액", 15)}: {self.real_nass_amt:,.0f} \n"
            f"  {align_left("전체 비중율", 15)}: {self.whol_weit_rt:,.0f}%"
        )


@dataclass(frozen=True)
class AccountBalances:
    balances: List[AccountBalance]

    @classmethod
    def from_dict(cls, data: dict):
        balances = [AccountBalance(**r) for r in data["output1"]]
        return cls(balances=balances)

    def __str__(self):
        return (
            f"[국내 주식]\n{self.balances[0]}\n"
            f"[해외 주식]\n{self.balances[7]}\n"
            f"[금현물]\n{self.balances[9]}\n"
            f"[예수금 잔고]\n{self.balances[15]}\n"
            f"[종합 잔고]\n{self.balances[18]}"
        )


cfg = Config()


def get_oversee_balance(
    access_token: str, oversee_exchange_code: str, currency_code: str
):
    headers = cfg.get_base_headers()
    headers["authorization"] = f"Bearer {access_token}"
    headers["appkey"] = cfg.AppKey
    headers["appsecret"] = cfg.SecretKey
    headers["tr_id"] = "TTTS3012R"

    params = {
        "CANO": cfg.Account,
        "ACNT_PRDT_CD": cfg.Product,
        "OVRS_EXCG_CD": oversee_exchange_code,
        "TR_CRCY_CD": currency_code,
        "CTX_AREA_FK200": "",
        "CTX_AREA_NK200": "",
    }

    res = get_request(
        api_url="/uapi/overseas-stock/v1/trading/inquire-balance",
        headers=headers,
        params=params,
    )
    if res.status_code != 200:
        print(f"error - {res.json()}")

    res_json = res.json()
    return res_json


def get_account_balance(access_token: str) -> AccountBalances:
    headers = cfg.get_base_headers()
    headers["authorization"] = f"Bearer {access_token}"
    headers["appkey"] = cfg.AppKey
    headers["appsecret"] = cfg.SecretKey
    headers["tr_id"] = "CTRP6548R"
    headers["custtype"] = "P"

    params = {
        "CANO": cfg.Account,
        "ACNT_PRDT_CD": cfg.Product,
        "INQR_DVSN_1": "",
        "BSPR_BF_DT_APLY_YN": "",
    }

    res = get_request(
        api_url="/uapi/domestic-stock/v1/trading/inquire-account-balance",
        headers=headers,
        params=params,
    )
    if res.status_code != 200:
        print(f"error - {res.json()}")

    res_json = res.json()
    return AccountBalances.from_dict(res_json)
