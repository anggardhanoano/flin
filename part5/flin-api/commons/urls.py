from django.urls import path
from commons.views.config import ConfigAPI
from commons.views.upload_file import UploadFileAPI


urlpatterns = [
    path("upload-file/", UploadFileAPI.as_view(), name="upload-file-api"),
    path("config/", ConfigAPI.as_view(), name='get-config'),
]
