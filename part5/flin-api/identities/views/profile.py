from identities.services.basic_authentication import BasicAuthenticationService
from drf_yasg.utils import swagger_auto_schema
from django.core.validators import validate_email
from rest_framework.fields import CharField, UUIDField
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from commons.schema import DomainGroup, create_ok_schema
from commons.serializers import ReadOnlySerializer
from rest_framework.views import APIView
from identities.services.profile import ProfileService


class ProfileAPI(APIView):

    class ProfileData(ReadOnlySerializer):
        id = UUIDField()
        email = CharField()
        full_name = CharField()
        phone_number = CharField(required=False)

    @swagger_auto_schema(
        responses=create_ok_schema(ProfileData()),
        tags=[DomainGroup.IDENTITIES],
        security=[],
    )
    def get(self, request: Request) -> Response:
        data = ProfileService.run(request.user)

        return Response(self.ProfileData(data).data)
