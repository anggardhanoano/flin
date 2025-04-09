from dataclasses import dataclass

from commons.dataclasses import BaseDataClass, JWTDataClass
from commons.patterns.runnable import Runnable
from identities.models import User
from identities.services.token_authentication import TokenAuthenticationService
from identities.socials.google import GoogleOauthProvider


class GoogleAuthenticationDataClass(BaseDataClass):
    token: JWTDataClass
    user: User
    is_new_user: bool


class GoogleAuthenticationService(Runnable):
    @classmethod
    def run(
        cls,
        access_token: str,
    ) -> GoogleAuthenticationDataClass:
        provider = GoogleOauthProvider()

        user, is_new_user = provider.get_social_user(access_token=access_token)

        token = TokenAuthenticationService.get_jwt_for_user(
            user=user,
        )

        return GoogleAuthenticationDataClass(
            token=token,
            user=user,
            is_new_user=is_new_user
        )
