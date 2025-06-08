import json
from typing import Dict


class Initializer:
    def __init__(self, key_path: str = "data/keys.json", curve_path: str = "data/p-256_parameters.json"):
        self.key_path: str = key_path
        self.curve_path: str = curve_path
        self.__key_param: Dict[str, int] = {}
        self.__curve_param: Dict[str, int] = {}

        self.__load_key()
        self.__load_curve()

    @property
    def key_param(self) -> Dict[str, int]:
        return self.__key_param

    @property
    def curve_param(self) -> Dict[str, int]:
        return self.__curve_param

    def __load_curve(self) -> Dict[str, int]:
        with open(self.curve_path, "r") as f:
            self.__curve_param = json.load(f)
        return self.__curve_param

    def __load_key(self) -> Dict[str, int]:
        with open(self.key_path, "r") as f:
            self.__key_param = json.load(f)
        return self.__key_param

