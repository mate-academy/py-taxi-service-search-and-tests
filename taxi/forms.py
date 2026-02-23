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


class DriverTitleSearchForm(forms.Form):
    driver = forms.CharField(max_length=255, required=False)


class CarModelSearchForm(forms.Form):
    model = forms.CharField(max_length=255, required=False)


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):  # this logic is optional, but possible
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            return license_number
        validate_license_number(license_number)
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            return license_number
        validate_license_number(license_number)
        return license_number


def validate_license_number(
    license_number,
):  # regex validation is also possible here
    if len(license_number) != 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number
