from typing import Dict

from rest_framework.serializers import BaseSerializer, Serializer

from commons.serializers import ErrorSerializer


def create_ok_schema(serializer: BaseSerializer, err_serializer=ErrorSerializer()) -> Dict[int, Serializer]:
    return {200: serializer, 400: err_serializer, 500: ErrorSerializer()}


class DomainGroup:
    COMMONS = "Commons"
    IDENTITIES = "Identities"
