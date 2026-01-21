from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


def validate_license_number(license_number):
    first_three = license_number[:3]

    if not first_three.isupper():
        raise ValidationError(
            "First 3 characters should be uppercase letters"
        )

    if len(license_number[3:]) != 5 or not license_number[3:].isdigit():
        raise ValidationError(
            "Last 5 characters should be digits"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = ["username", "password1", "password2", "license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        validate_license_number(license_number)  # Виклик функції валідації
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(max_length=200, label="Search by name")


class CarSearchForm(forms.Form):
    model = forms.CharField(max_length=200, label="Search by model")


class DriverSearchForm(forms.Form):
    license_number = forms.CharField(
        max_length=10,
        label="Search by license number"
    )
