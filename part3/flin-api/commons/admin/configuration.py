
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from commons.admin.admin_base import BaseAdmin
from commons.models.configuration import Configuration
from django.db import models


@admin.register(Configuration)
class ConfigurationAdmin(BaseAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
