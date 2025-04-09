from typing import Tuple

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token

from commons.exceptions import ForbiddenRequestException
from identities.models.user import User
from identities.socials.base import SocialProvider


class GoogleOauthProvider(SocialProvider):

    GOOGLE_USER_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_social_user(self, access_token: str) -> Tuple[User, bool]:
        raw_google_user = self._request(
            self.GOOGLE_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        json_user = self._parse_raw_user(raw_user_data=raw_google_user)

        if User.objects.filter(email=json_user["email"]).first():
            user: User = User.objects.filter(
                email=json_user["email"].lower()).first()

            if user.provider != User.ProviderTypes.GOOGLE:
                if user.provider == User.ProviderTypes.BASIC:
                    raise ForbiddenRequestException(
                        f"This User Login with Email and Password, please try again by using your email and password"
                    )
                else:
                    raise ForbiddenRequestException(
                        f"This User Login with {user.provider} provider, please try again with {user.provider} provider"
                    )

            return user, False

        user = User.objects.create(**json_user)

        return user, True

    def _parse_raw_user(self, raw_user_data):

        return {
            "email": raw_user_data.get("email").lower(),
            "phone_number": raw_user_data.get("phone_number", ""),
            "full_name": raw_user_data.get("name", ""),
            "provider": User.ProviderTypes.GOOGLE,
            "is_email_verified": True,
            "is_active": True,
        }


class MobileGoogleOAuthProvider(SocialProvider):
    """Google OAuth2 Social Provider"""

    def get_social_user(self, access_token, *args, **kwargs) -> Tuple[User, bool]:
        """Retrieves user data from Google API"""
        client_id = settings.GOOGLE_CONFIG.get("CLIENT_ID_MOBILE")
        user_data = id_token.verify_oauth2_token(
            id_token=access_token, request=requests.Request(), audience=client_id)
        json_user = self._parse_raw_user(raw_user_data=user_data)

        if User.objects.filter(email=json_user["email"]).first():
            user: User = User.objects.filter(
                email=json_user["email"].lower()).first()

            if user.provider != User.ProviderTypes.GOOGLE:

                if user.provider == User.ProviderTypes.BASIC:
                    raise ForbiddenRequestException(
                        f"This User Login with Email and Password, please try again by using your email and password"
                    )
                else:
                    raise ForbiddenRequestException(
                        f"This User Login with {user.provider} provider, please try again with {user.provider} provider"
                    )

            return user, False

        user = User.objects.create(**json_user)

        return user, True

    def _parse_raw_user(self, raw_user_data):

        return {
            "email": raw_user_data.get("email").lower(),
            "phone_number": raw_user_data.get("phone_number", ""),
            "full_name": raw_user_data.get("name", ""),
            "provider": User.ProviderTypes.GOOGLE,
            "is_email_verified": True,
            "is_active": True,
        }
