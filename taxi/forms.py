from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver, Manufacturer


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    image = forms.ImageField(
        label="Select image for car",
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number


class DriversSearchForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search..."})
    )


class CarsSearchForm(forms.Form):
    model = forms.CharField(
        required=True,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search..."})
    )


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search..."})
    )


class ManufacturerForm(forms.ModelForm):
    logo = forms.ImageField(
        label="",
        required=False
    )

    class Meta:
        model = Manufacturer
        fields = "__all__"
