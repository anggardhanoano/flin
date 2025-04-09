from typing import Any

from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import set_rollback

from commons.dataclasses import BaseDataClass


class ErrorResponse(BaseDataClass):
    error_message: Any = "Something went wrong."
    code: Any = None
    validation_error: Any = None


def custom_exception_handler(exc, context):
    """
    Extended from from rest_framework.views.exception_handler
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py#L71

    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc, exceptions.ValidationError):
            data = ErrorResponse(
                validation_error=exc.detail, code=exc.default_code)
        else:
            data = ErrorResponse(error_message=exc.detail,
                                 code=exc.get_codes())
        complete_data = dict(errors=data.dict())

        set_rollback()
        return Response(data=complete_data, status=exc.status_code, headers=headers)

    return None
