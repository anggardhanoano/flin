from typing import Optional
from django.http import QueryDict

from commons.dataclasses import BaseDataClass
from commons.utils import get_query_param


class ListQueryParams(BaseDataClass):
    page: Optional[int] = None
    limit: int


def parse_query_param(params: QueryDict) -> ListQueryParams:
    page = None
    limit = 10

    limit_val = get_query_param(params, "limit")
    if limit_val:
        if not limit_val.isnumeric():
            raise ValueError("Limit is not a number")
        limit_val = int(limit_val)
        if limit_val > 0:
            limit = limit_val

    page_val = get_query_param(params, "page")
    if page_val:
        if not page_val.isnumeric():
            raise ValueError("Page is not a number")
        page_val = int(page_val)
        if page_val > 0:
            page = page_val

    return ListQueryParams(
        page=page,
        limit=limit,
    )
