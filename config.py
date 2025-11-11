import json
import copy


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        with open("configs.json") as config_json_file:
            configs = json.load(config_json_file)
            self.BaseURL = configs["BaseURL"]
            self.ID = configs["ID"]
            self.AppKey = configs["AppKey"]
            self.SecretKey = configs["SecretKey"]
            self.Account = configs["Account"]
            self.Product = configs["Product"]

        self.BaseHeaders = {
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "charset": "UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

    def get_base_headers(self):
        return copy.deepcopy(self.BaseHeaders)
