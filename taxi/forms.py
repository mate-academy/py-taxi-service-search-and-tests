import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


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


def validate_license_number(license_number):
    pattern = r"^[A-Z]{3}\d{5}$"

    if not re.fullmatch(pattern, license_number):
        raise forms.ValidationError(
            "License number must be 8 characters: first 3 uppercase "
            "letters followed by 5 digits (e.g., ABC12345)."
        )
    return license_number


class DriverSearchForm(forms.Form):
    username = forms.CharField(max_length=255, required=False)


class CarSearchForm(forms.Form):
    model = forms.CharField(max_length=255, required=False)


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
