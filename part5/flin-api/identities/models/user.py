import uuid
from ast import arg

import phonenumbers
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from phonenumbers.phonenumberutil import (NumberParseException,
                                          PhoneNumberFormat)

from commons.base_model import BaseModel
from commons.exceptions import BadRequestException


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        phone_number="",
        full_name="",
        password=None,
        is_active=True,
        should_allow_incomplete=False,
    ):

        if len(full_name) > 256:
            raise ValueError("Full name must be 256 characters or fewer.")

        if not email and not should_allow_incomplete:
            raise ValueError("Email Required")

        if phone_number != "":
            phone_number = self.format_phone_number(phone_number)

            if phone_number and not (8 <= len(phone_number) <= 16):
                raise ValueError("Wrong Phone Number Format")

        user = self.model(email=self.normalize_email(email.lower()) or None)
        user.phone_number = phone_number
        user.full_name = full_name
        user.is_active = is_active

        if password:
            user.set_password(password)

        user.save()

        return user

    def create_superuser(self,
                         email,
                         phone_number="",
                         full_name="",
                         password=None
                         ):

        user = self.create_user(
            phone_number=phone_number,
            email=email,
            full_name=full_name,
            password=password,
            is_active=True,
        )

        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def update_user(self, **kwargs):
        full_name = kwargs.get("full_name")
        if full_name and len(full_name) > 256:
            raise ValueError("Full name must be 256 characters or fewer.")

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        try:
            self.save()
        except Exception as e:
            raise ValueError("An error occurred while saving: " + str(e))

    @classmethod
    def format_phone_number(cls, phone_number):
        """
        Format phone number to the standard E.164 international format.
        """
        try:
            parsed_pnumber = phonenumbers.parse(phone_number, "ID")
        except NumberParseException:
            raise BadRequestException(
                "Invalid phone number format"
            )

        return phonenumbers.format_number(parsed_pnumber, PhoneNumberFormat.E164)


# TODO: Adjust with your needs
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class ProviderTypes:
        BASIC = "basic"
        GOOGLE = "google"

    class GenderType(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    # TODO
    PROVIDER_CHOICES = {
        ProviderTypes.BASIC: "Basic",
        ProviderTypes.GOOGLE: "Google",
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=256)

    email = models.EmailField(unique=True, null=False, default=None)
    username = models.CharField(max_length=64, unique=True)

    phone_number = models.CharField(max_length=16, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    provider = models.CharField(
        max_length=32, choices=PROVIDER_CHOICES.items(), default=ProviderTypes.BASIC
    )
    gender = models.CharField(
        max_length=16, choices=GenderType.choices, blank=True)
    birthdate = models.DateField(blank=True, null=True)

    objects = UserManager()

    # TODO: if you want user to login with email/username/phone_number
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    @property
    def photo_profile(self):

        if hasattr(self, 'student'):
            return self.student.photo_profile

        return None

    class Meta:
        db_table = "user"
        verbose_name = "User"

    def __str__(self):
        return self.email
