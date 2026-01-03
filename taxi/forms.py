from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver

LICENSE_ERRORS = {
    1: "License number should consist of 8 characters",
    2: "First 3 characters should be uppercase letters",
    3: "Last 5 characters should be digits",
}


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search car"}
        )
    )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):  # this logic is optional, but possible
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverSearchForm(forms.Form):
    driver = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search driver"}
        )
    )


class ManufacturerSearchForm(forms.Form):
    manufacturer = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search manufacturer"}
        )
    )


def validate_license_number(
    license_number,
):  # regex validation is also possible here
    if len(license_number) != 8:
        raise ValidationError(LICENSE_ERRORS[1])
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError(LICENSE_ERRORS[2])
    elif not license_number[3:].isdigit():
        raise ValidationError(LICENSE_ERRORS[3])

    return license_number
