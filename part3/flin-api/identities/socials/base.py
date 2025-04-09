from requests import request

from identities.models.user import User


class SocialProvider:
    @classmethod
    def get_social_user(self, access_token: str) -> User:
        raise NotImplementedError

    def _request(self, url, method="GET", *args, **kwargs):
        response = request(method, url, *args, **kwargs)

        response.raise_for_status()
        return response.json()
