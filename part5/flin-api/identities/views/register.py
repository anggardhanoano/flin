from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core.validators import validate_email
from rest_framework.fields import CharField
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.schema import DomainGroup, create_ok_schema
from commons.serializers import ReadOnlySerializer
from identities.serializers import SocialAuthResponse
from identities.services.registration import RegistrationService


class RegisterAPI(APIView):
    permission_classes = (AllowAny,)

    # TODO: if using phone number instead email, please adjust
    class RegisterInputData(ReadOnlySerializer):
        email = CharField(validators=[validate_email])
        password = CharField()

    @swagger_auto_schema(
        request_body=RegisterInputData(),
        responses=create_ok_schema(SocialAuthResponse()),
        tags=[DomainGroup.IDENTITIES],
        security=[],
    )
    def post(self, request: Request, **kwargs) -> Response:
        serializer = self.RegisterInputData(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = RegistrationService.run(
            **serializer.validated_data)

        return Response(SocialAuthResponse(new_user).data)
