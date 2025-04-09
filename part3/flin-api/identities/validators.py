from rest_framework import serializers

from identities.constants import (
    GENDER_IS_NOT_RECOGNIZED)
from identities.models import User


def gender_validator(value: str):
    if User.GenderType[value] is None:
        return serializers.ValidationError(GENDER_IS_NOT_RECOGNIZED)
