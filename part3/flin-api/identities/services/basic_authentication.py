from django.contrib.auth import authenticate

from commons.dataclasses import BaseDataClass, JWTDataClass
from commons.exceptions import BadRequestException, ForbiddenRequestException
from commons.patterns.runnable import Runnable
from identities.constants import INACTIVE_ACCOUNT, WRONG_CREDENTIALS
from identities.models import User
from identities.services.token_authentication import TokenAuthenticationService


class BasicAuthenticationDataClass(BaseDataClass):
    token: JWTDataClass
    user: User


class BasicAuthenticationService(Runnable):
    @classmethod
    def authenticate_user(cls, email: str, password: str) -> User:
        check_user = User.objects.filter(email=email.lower())

        if not check_user.first():
            raise BadRequestException(WRONG_CREDENTIALS)

        if check_user.first() and check_user[0].provider != User.ProviderTypes.BASIC:
            raise ForbiddenRequestException(
                f"This User Login with {check_user[0].provider} provider, please try again with {check_user[0].provider} provider"
            )

        auth_user: User = authenticate(email=email.lower(), password=password)

        if not auth_user:
            raise BadRequestException(WRONG_CREDENTIALS)

        if not auth_user.is_active:
            raise BadRequestException(INACTIVE_ACCOUNT)

        return auth_user

    @classmethod
    def run(
        cls,
        email: str,
        password: str
    ) -> BasicAuthenticationDataClass:
        user = cls.authenticate_user(email, password)

        token = TokenAuthenticationService.get_jwt_for_user(
            user=user,
        )

        return BasicAuthenticationDataClass(
            token=token,
            user=user,
        )
