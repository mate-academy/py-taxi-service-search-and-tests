import re
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


def validate_license_number(license_number: str) -> None:
    if not re.fullmatch(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "License number has to be 8 characters long, "
            "first 3 characters have to be uppercase, "
            "5 last characters have to be digits"
        )


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[validate_license_number],
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (  # type: ignore
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=255,
        validators=[validate_license_number],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model"}),
    )


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
