from drf_yasg.utils import swagger_auto_schema
from rest_framework.fields import CharField
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from commons.serializers import ReadOnlySerializer
from commons.schema import DomainGroup, create_ok_schema

from identities.serializers import SocialAuthResponse
from identities.services.google_authentication import GoogleAuthenticationService


class GoogleLoginAPI(APIView):
    permission_classes = (AllowAny,)

    class GoogleLoginInputData(ReadOnlySerializer):
        access_token = CharField()

    @swagger_auto_schema(
        request_body=GoogleLoginInputData(),
        responses=create_ok_schema(SocialAuthResponse()),
        tags=[DomainGroup.IDENTITIES],
        security=[],
    )
    def post(self, request: Request, **kwargs) -> Response:
        serializer = self.GoogleLoginInputData(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_user = GoogleAuthenticationService.run(
            access_token=serializer.validated_data["access_token"],
        )

        return Response(SocialAuthResponse(login_user).data)
