import os
import sys
from typing import Dict, List, Union


def load_env(list_key: List[str], root_key: str) -> Dict[str, Union[str, None]]:

    if os.getenv("ENVIRONMENT") == "ci":
        return dict()
    data: Dict[str, Union[str, None]] = dict()
    for i in list_key:
        env_key = f"{root_key}_{i}"
        val: Union[str, None] = os.getenv(env_key)
        if val is None:
            print(f"{env_key} is required")
            sys.exit(1)
        data[i] = val

    return data
