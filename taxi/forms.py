import random

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


class CarModelSearchForm(forms.Form):
    example_list = [
        "T, Yaris, toy",
        "Ford, Focus, ford",
        "Mi, lancer, mits",
        "Lincoln, MKZ, lincoln",
    ]

    def __init__(self, *args, **kwargs):
        super(CarModelSearchForm, self).__init__(*args, **kwargs)
        self.fields["model_"].widget.attrs[
            "placeholder"
        ] = f"ex: {random.choice(self.example_list)}"

    model_ = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriversUsernameSearchForm(forms.Form):
    example_list = [
        "john, JOHN, joh",
        "mike, MIKE, MI",
        "alex, ALEX, a",
        "bob, BOB, bo",
        "alice, ALICE, ALI",
    ]

    def __init__(self, *args, **kwargs):
        super(DriversUsernameSearchForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = f"ex: {random.choice(self.example_list)}"

    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )


class ManufacturersNameSearchForm(forms.Form):
    example_list = [
        "BMW, bMW, bmw",
        "FCA, fCA",
        "Ford, ford",
        "Mitsubishi, mits",
        "Lin, LINCOLN",
    ]

    def __init__(self, *args, **kwargs):
        super(ManufacturersNameSearchForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs[
            "placeholder"
        ] = f"ex: {random.choice(self.example_list)}"

    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(),
    )


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
