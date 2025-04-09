from identities.services.basic_authentication import BasicAuthenticationService
from drf_yasg.utils import swagger_auto_schema
from django.core.validators import validate_email
from rest_framework.fields import CharField
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from commons.schema import DomainGroup, create_ok_schema
from rest_framework.views import APIView


from commons.serializers import ReadOnlySerializer
from identities.serializers import AuthResponse


class BasicLoginAPI(APIView):
    permission_classes = (AllowAny,)

    class BasicLoginInputData(ReadOnlySerializer):
        email = CharField(validators=[validate_email])
        password = CharField()

    @swagger_auto_schema(
        request_body=BasicLoginInputData(),
        responses=create_ok_schema(AuthResponse()),
        tags=[DomainGroup.IDENTITIES],
        security=[],
    )
    def post(self, request: Request) -> Response:
        serializer = self.BasicLoginInputData(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_user = BasicAuthenticationService.run(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(AuthResponse(login_user).data)
