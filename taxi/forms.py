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


class DriverUsernameSearchForm(forms.Form):
    username = forms.CharField(
        label="",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not get_user_model().objects.filter(username=username).exists():
            raise ValidationError("User with this username does not exist")
        return username


class CarModelSearchForm(forms.Form):
    model = forms.CharField(
        label="",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Enter model"}),
    )

    def clean_model(self):
        model = self.cleaned_data["model"]
        if not Car.objects.filter(model=model).exists():
            raise ValidationError("Car with this model does not exist")
        return model


class ManufacturerNameSearchForm(forms.Form):
    manufacturer = forms.CharField(
        label="",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
    )
