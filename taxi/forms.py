from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


DRIVER_LICENSE_VALIDATOR = RegexValidator(
    regex=r"^[A-Z]{3}[\d]{5}$",
    message="Enter a valid value license number:"
            " 1.Consist only of 8 characters"
            " 2.First 3 characters are uppercase letters"
            " 3.Last 5 characters are digits", )


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        validators=[DRIVER_LICENSE_VALIDATOR, ]
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
        required=True,
        validators=[DRIVER_LICENSE_VALIDATOR, ]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverNicknameSearchForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)


class CarModelSearchForm(forms.Form):
    model = forms.CharField(max_length=50, required=False)


class ManufacturerNameSearchForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
