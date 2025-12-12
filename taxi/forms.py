from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car

Driver = get_user_model()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["drivers"].queryset = Driver.objects.all()


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data.get("license_number"))


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data.get("license_number"))


def validate_license_number(license_number):
    if license_number is None:
        raise ValidationError("License number is required.")

    license_number = str(license_number).strip()

    if len(license_number) != 8:
        raise ValidationError("License number should consist of 8 characters.")

    first3, last5 = license_number[:3], license_number[3:]

    if not first3.isalpha() or first3 != first3.upper():
        raise ValidationError("First 3 character"
                              "s should be uppercase letters.")

    if not last5.isdigit():
        raise ValidationError("Last 5 characters should be digits.")

    return license_number


class DriverSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
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
