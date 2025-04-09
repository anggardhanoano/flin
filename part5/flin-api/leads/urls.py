# please implement the url api based on the views

from django.urls import path
from leads.views.create_list_inquiry import CreateListInquiryAPI
from leads.views.list_inquiries import ListInquiriesAPI

urlpatterns = [
    # path("", ListInquiriesAPI.as_view(), name="list_inquiries"),
    path("", CreateListInquiryAPI.as_view(), name="create_inquiry"),
]
