import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


license_number_validator = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number must consist of "
            "3 uppercase letters followed by 5 digits."
)


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[license_number_validator],
        label="License number")

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if Driver.objects.filter(license_number=license_number).exists():
            if (self.instance
                    and self.instance.license_number == license_number):
                pass
            else:
                raise forms.ValidationError(
                    "A driver's license "
                    "with this number already exists."
                )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


def validate_license_number(
    license_number,
):  # regex validation is also possible here
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise ValidationError(
            "The license number must consist of 3 "
            "capital letters and 5 digits."
        )
    return license_number
