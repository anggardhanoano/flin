from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.schema import create_ok_schema, DomainGroup
from commons.serializers import ReadOnlySerializer
from commons.services.get_configuration import GetConfigurationService
from commons.utils import get_query_param
from rest_framework.permissions import AllowAny

class ConfigAPI(APIView):
    permission_classes = (AllowAny,)

    class GetConfigResponseData(ReadOnlySerializer):
        class Meta:
            ref_name = "Get config response data"
        configs = serializers.DictField()

    @swagger_auto_schema(
        responses=create_ok_schema(GetConfigResponseData()),
        tags=[DomainGroup.COMMONS],
        operation_description="This endpoint is to get upload links to S3 bucket without using File schema on database,\
             available bucket_keys are: PUBLIC",
    )
    def get(self, request: Request, **kwargs) -> Response:

        config = GetConfigurationService.get_all_config()

        return Response(self.GetConfigResponseData(config).data)
