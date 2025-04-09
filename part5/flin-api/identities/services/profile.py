from commons.patterns.runnable import Runnable


class ProfileDataClass:
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
            full_name=user.full_name,
            phone_number=user.phone_number,
            email=user.email,
        )
