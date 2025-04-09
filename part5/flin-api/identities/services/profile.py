from uuid import UUID
from commons.patterns.runnable import Runnable
from commons.dataclasses import BaseDataClass


class ProfileDataClass(BaseDataClass):
    id: UUID
    full_name: str
    phone_number: str
    email: str


class ProfileService(Runnable):
    @classmethod
    def run(
        cls,
        user,
    ) -> ProfileDataClass:
        return ProfileDataClass(
            id=user.id,
            full_name=user.full_name,
            phone_number=user.phone_number,
            email=user.email,
        )
