from django import forms
from django.core.validators import URLValidator
from django.db.models import URLField


class BaseURLField(URLField):
    default_validators = [URLValidator()]
    description = "URL"

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        return super().formfield(
            **{
                "form_class": forms.URLField,
                "widget": forms.URLField,
                **kwargs,
            }
        )
