from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from commons.schema import create_ok_schema
from leads.services.user_inquiries import UserInquiriesService
from leads.serializers import InquiryResponseData
from commons.query_params_parser import parse_query_param
from commons.serializers import BasePaginationSerializer


class CreateListInquiryAPI(APIView):
    permission_classes = [AllowAny]

    class InquiryInputData(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        email = serializers.EmailField()
        phone_number = serializers.CharField(max_length=20)
        loan_type = serializers.ChoiceField(choices=[
            ("personal", "Personal Loan"),
            ("kpr", "KPR"),
            ("kpa", "KPA")
        ])

    class ListInquiriesResponseData(BasePaginationSerializer):
        data = InquiryResponseData(many=True)

    @swagger_auto_schema(
        responses=create_ok_schema(InquiryResponseData()),
        tags=["Leads"],
    )
    def post(self, request):
        serializer = self.InquiryInputData(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = UserInquiriesService.create_user_inquiry(
            name=serializer.validated_data["name"],
            email=serializer.validated_data["email"],
            phone_number=serializer.validated_data["phone_number"],
            loan_type=serializer.validated_data["loan_type"]
        )
        response_serializer = InquiryResponseData(lead)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses=create_ok_schema(ListInquiriesResponseData()),
        tags=["Leads"],
    )
    def get(self, request, **kwargs):

        if request.user.is_anonymous:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        query_params = parse_query_param(request.GET)
        data = UserInquiriesService.get_all_user_inquiry(
            **query_params.model_dump())

        return Response(self.ListInquiriesResponseData(data).data)
