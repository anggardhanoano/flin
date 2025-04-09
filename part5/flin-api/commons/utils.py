from datetime import datetime, timedelta
import random
import string
import string
from typing import Any, Optional
from django.http import QueryDict
from itertools import islice


def get_query_param(queries: QueryDict, key: str, default: Any = None) -> Optional[str]:
    val = queries.get(key, default)
    if type(val) is str:
        if len(val) == 0:
            return default
    return val


def is_not_none_and_empty_string(data) -> bool:
    return data is not None and data != ''


def generate_random_string(length: int):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))


def get_hours_from_now(h: int):
    return datetime.now() + timedelta(hours=h)
