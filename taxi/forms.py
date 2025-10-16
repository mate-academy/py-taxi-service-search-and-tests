from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car

custom_code_validator = RegexValidator(
    regex=r"^[A-Z]{3}[0-9]{5}$",
    message="Enter exactly 8 characters: "
    "3 uppercase letters followed by 5 digits.",
    code="invalid_code",
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[custom_code_validator],
        help_text="Format: ABC12345",
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[custom_code_validator],
        help_text="Format: ABC12345",
    )

    class Meta:
        model = get_user_model()
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


# -----------search---------------
class DriverSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="Model",
        widget=forms.TextInput(attrs={"placeholder": "Search by Model"}),
    )


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by Name of Manufacturer"}
        ),
    )
