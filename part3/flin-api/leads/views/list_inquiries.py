from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from commons.schema import create_ok_schema
from commons.query_params_parser import parse_query_param
from commons.serializers import BasePaginationSerializer
from leads.services.user_inquiries import UserInquiriesService
from leads.serializers import InquiryResponseData
from rest_framework.permissions import IsAuthenticated


class ListInquiriesAPI(APIView):
    permission_classes = [IsAuthenticated]

    class ListInquiriesResponseData(BasePaginationSerializer):
        data = InquiryResponseData(many=True)

    @swagger_auto_schema(
        responses=create_ok_schema(ListInquiriesResponseData()),
        tags=["Leads"],
    )
    def get(self, request, **kwargs):
        query_params = parse_query_param(request.GET)
        data = UserInquiriesService.get_all_user_inquiry(
            **query_params.model_dump())

        return Response(self.ListInquiriesResponseData(data).data)
