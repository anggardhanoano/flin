from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


from commons.patterns.runnable import Runnable
from commons.dataclasses import JWTDataClass
from identities.models.user import User


class TokenAuthenticationService(Runnable):
    @classmethod
    def generate_token(cls, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    @classmethod
    def get_jwt_for_user(cls, user: User) -> JWTDataClass:
        refresh = RefreshToken.for_user(user)

        return JWTDataClass(
            refresh=str(refresh),
            access=str(refresh.access_token),
        )
