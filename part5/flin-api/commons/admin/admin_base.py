from django.contrib import admin
from django.contrib.admin.widgets import AdminURLFieldWidget
from commons.fields.url_field import BaseURLField


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BaseURLField: {"widget": AdminURLFieldWidget},
    }


class HiddenBaseAdmin(BaseAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class BaseStackedInlineAdmin(admin.StackedInline):
    formfield_overrides = {
        BaseURLField: {"widget": AdminURLFieldWidget},
    }
    show_change_link = True
    extra = 0

    class Meta:
        abstract = True


class BaseTabularInlineAdmin(admin.TabularInline):
    formfield_overrides = {
        BaseURLField: {"widget": AdminURLFieldWidget},
    }
    show_change_link = True
    extra = 0

    class Meta:
        abstract = True
