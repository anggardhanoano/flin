from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import authentication, permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger API",
        default_version="v1",
        description="Authorize with format 'Token <your-token>'",
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    authentication_classes=(authentication.BasicAuthentication,),
)()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger")),
    path("identities/", include("identities.urls")),
    path("commons/", include('commons.urls')),
    path("leads/", include("leads.urls"))
]
