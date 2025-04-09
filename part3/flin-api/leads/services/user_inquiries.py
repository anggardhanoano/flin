from typing import List
from uuid import UUID
from commons.patterns.runnable import Runnable
from commons.dataclasses import BaseDataClass
from commons.paginations import BasePaginationDataClass, paginate_queryset
from identities.models.user import UserManager
from leads.models.lead import Lead


class UserInquiryDataClass(BaseDataClass):
    id: UUID
    name: str
    email: str
    phone_number: str
    loan_type: Lead.LoanType


class UserInquiriesDataClass(BasePaginationDataClass):
    data: List[UserInquiryDataClass]


class UserInquiriesService(Runnable):

    @classmethod
    def create_user_inquiry(cls, name: str, email: str, phone_number: str, loan_type: Lead.LoanType) -> UserInquiryDataClass:

        new_lead = Lead.objects.create(
            name=name,
            email=email,
            phone_number=UserManager.format_phone_number(phone_number),
            loan_type=loan_type
        )

        return UserInquiryDataClass(
            id=new_lead.id,
            name=new_lead.name,
            email=new_lead.email,
            phone_number=new_lead.phone_number,
            loan_type=new_lead.loan_type
        )

    @classmethod
    def get_user_inquiry(cls, lead_id: UUID) -> UserInquiryDataClass:
        lead = Lead.objects.get(id=lead_id)
        return UserInquiryDataClass(
            id=lead.id,
            name=lead.name,
            email=lead.email,
            phone_number=lead.phone_number,
            loan_type=lead.loan_type
        )

    @classmethod
    def get_all_user_inquiry(cls, page: int, limit: int = 10, **kwargs) -> UserInquiriesDataClass:
        leads = Lead.objects.all()

        pagination = paginate_queryset(leads, page, limit)
        leads = pagination.queryset
        count_items = pagination.count_items
        next_page = pagination.next_page
        previous_page = pagination.previous_page

        return UserInquiriesDataClass(
            data=[
                UserInquiryDataClass(
                    id=lead.id,
                    name=lead.name,
                    email=lead.email,
                    phone_number=lead.phone_number,
                    loan_type=lead.loan_type
                ) for lead in leads
            ],
            count_items=count_items,
            next_page=next_page,
            previous_page=previous_page
        )
