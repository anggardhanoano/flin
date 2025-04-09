from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.schema import DomainGroup, create_ok_schema
from commons.serializers import ReadOnlySerializer
from commons.services.upload_file import UploadFileRequestData, UploadFileService


class UploadFileAPI(APIView):
    permission_classes = [IsAuthenticated]

    class UploadFileRequestV2(ReadOnlySerializer):
        file_names = serializers.ListField(
            min_length=1, max_length=10, child=serializers.CharField()
        )
        bucket_key = serializers.CharField()

        def validate_file_names(self, file_names):
            requested_file_names = set(file_names)

            if len(requested_file_names) != len(file_names):
                raise serializers.ValidationError(
                    "Duplicated file names are not allowed."
                )
            return file_names

    class UploadFileOuterResponseV2(ReadOnlySerializer):
        class UploadFileResponseV2(ReadOnlySerializer):
            class PresignedDataV2(ReadOnlySerializer):
                upload_url = serializers.URLField()
                fields = serializers.DictField()

            file_name = serializers.CharField()
            file_url = serializers.CharField()
            file_extension = serializers.CharField()
            file_path = serializers.CharField()
            presigned_data = PresignedDataV2()

        data = serializers.ListField(child=UploadFileResponseV2())

    @swagger_auto_schema(
        request_body=UploadFileRequestV2(),
        responses=create_ok_schema(UploadFileOuterResponseV2()),
        tags=[DomainGroup.COMMONS],
        operation_description="This endpoint is to get upload links to S3 bucket without using File schema on database,\
             available bucket_keys are: PUBLIC",
    )
    def post(self, request: Request, **kwargs) -> Response:
        serializer = self.UploadFileRequestV2(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload_request = UploadFileRequestData(**serializer.data)

        with transaction.atomic():
            data = UploadFileService.run(upload_request)
            current_data = self.UploadFileOuterResponseV2(data)
            return Response(current_data.data)
