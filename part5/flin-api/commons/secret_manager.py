from typing import List, Dict, Union
from dotenv import load_dotenv
import sys

import os


class SecretManager:

    def __init__(self):
        load_dotenv()

    def get_env(self, key, default_value=None, not_strict=False):
        variable = os.getenv(key, default_value)

        if variable is None and not not_strict:
            print(f"Key not provided: {key}")
            sys.exit(1)

        return os.getenv(key, default_value)

    def get_bulk_env(self, list_key: List[str], root_key: str) -> Dict[str, Union[str, None]]:
        data: Dict[str, Union[str, None]] = dict()
        for i in list_key:
            env_key = f"{root_key}_{i}"
            val: Union[str, None] = self.get_env(env_key)
            data[i] = val

        return data
