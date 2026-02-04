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
    # pattern:
    # ^ - the beginning of the line
    # [A-Z]{3} - exactly 3 capital letters
    # \d{5} - exactly 5 digits
    # $ - end of line
    pattern = r"^[A-Z]{3}\d{5}$"

    if not re.match(pattern, license_number):
        raise ValidationError(
            "License number must be 8 characters:"
            " 3 uppercase letters followed by 5 digits."
        )

    return license_number


class DriverSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search Drivers by Username",
                "style": "width:33vw"
            },
        ),
    )


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search Cars by Model",
                "style": "width:33vw"
            },
        ),
    )


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search Manufacturer by Name",
                "style": "width:33vw"
            },
        ),
    )
