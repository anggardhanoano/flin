from rest_framework import serializers, status
from commons.serializers import ReadOnlySerializer


class InquiryResponseData(ReadOnlySerializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    loan_type = serializers.ChoiceField(choices=[
        ("personal", "Personal Loan"),
        ("kpr", "KPR"),
        ("kpa", "KPA")
    ])
