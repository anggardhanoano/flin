from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.core.exceptions import ValidationError
from rangefilter.filters import DateRangeFilter

from identities.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        password = self.fields.get("password")
        if password:
            password_help_text = "Change user password"
            password.help_text = f"<a href='../password/'>{password_help_text}</a>"

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "full_name",
            "username",
            "provider",
            "is_staff",
            "is_superuser",
        )


@admin.register(User)
class IdentityAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        "email",
        "phone_number",
        "username",
        "full_name",
        "provider",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (None, {"fields": ("email", "full_name", "phone_number", "username")}),
        ("Personal info", {"fields": ("birthdate", "password",)}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "groups", "is_superuser")},
        ),
    )
    list_filter = ('gender',
                   ('created_at', DateRangeFilter), ('updated_at', DateRangeFilter))
    search_fields = ['email',
                     'phone_number', 'full_name', 'username']
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "phone_number",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    ordering = ("-updated_at",)
