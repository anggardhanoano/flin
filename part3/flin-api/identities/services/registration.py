from dataclasses import dataclass
from typing import Optional

from django.db import IntegrityError
from commons.dataclasses import BaseDataClass, JWTDataClass
from identities.services.token_authentication import TokenAuthenticationService

from commons.exceptions import BadRequestException
from commons.patterns.runnable import Runnable
from identities.constants import EMAIL_ALREADY_EXIST
from identities.models.user import User


class RegistrationDataClass(BaseDataClass):
    token: JWTDataClass
    user: User
    is_new_user: bool


# TODO: if user needs phone number instead email, please adjust
class RegistrationService(Runnable):
    @classmethod
    def run(
        cls,
        email: str,
        password: str,
        full_name: Optional[str] = "",
    ) -> RegistrationDataClass:
        try:
            new_user: User = User.objects.create_user(
                email=email.lower(), password=password, full_name=full_name
            )
        except IntegrityError as e:
            print(str(e))
            raise BadRequestException(EMAIL_ALREADY_EXIST)
        except Exception as e:
            raise BadRequestException(str(e))

        return RegistrationDataClass(
            user=new_user,
            token=TokenAuthenticationService.get_jwt_for_user(
                user=new_user,
            ),
            is_new_user=True,
        )
