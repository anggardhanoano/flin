from rest_framework.fields import BooleanField, CharField

from commons.serializers import ReadOnlySerializer
from rest_framework import serializers

from identities.models.user import User


class UserAuthData(ReadOnlySerializer):
    id = CharField()
    full_name = CharField(allow_blank=True, required=False)
    email = CharField()
    phone_number = CharField()
    photo_profile = serializers.SerializerMethodField()
    username = CharField(allow_blank=True, required=False)
    provider = CharField()
    is_email_verified = BooleanField(allow_null=True, default=False)

    def get_photo_profile(self, obj: User):
        return obj.photo_profile


class JWTData(ReadOnlySerializer):
    refresh = CharField()
    access = CharField()


class AuthResponse(ReadOnlySerializer):
    user = UserAuthData()
    token = JWTData()


class SocialAuthResponse(AuthResponse):
    is_new_user = BooleanField(allow_null=True, default=False)
