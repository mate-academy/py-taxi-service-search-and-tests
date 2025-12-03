from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taxi.models import Car, Driver

User = get_user_model()


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=100,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "aria-label": "search",
                "class": "form-control",
            }
        ),
    )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
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

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            raise ValidationError("License number is required.")
        return validate_license_number(license_number)


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if not license_number:
            raise ValidationError("License number is required.")
        return validate_license_number(license_number)


def validate_license_number(license_number):
    if not isinstance(license_number, str):
        raise ValidationError("Invalid license number format.")
    if len(license_number) != 8:
        raise ValidationError("License number should consist of 8 characters")
    prefix = license_number[:3]
    suffix = license_number[3:]
    if not prefix.isalpha() or not prefix.isupper():
        raise ValidationError("First 3 characters should be uppercase letters")
    if not suffix.isdigit():
        raise ValidationError("Last 5 characters should be digits")
    return license_number
