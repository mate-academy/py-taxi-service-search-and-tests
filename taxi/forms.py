from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple, )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = (UserCreationForm.Meta.fields
                  + ("license_number", "first_name", "last_name",))

    def clean_license_number(self):  # this logic is optional, but possible
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

    first_part = license_number[:3]
    second_part = license_number[3:]

    if not first_part.isupper() or not first_part.isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")

    if not second_part.isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return license_number


class DriverSearchForm(forms.Form):
    user_name = forms.CharField(max_length=255, required=False, label="",
                                widget=forms.TextInput(
                                    attrs={"class": "form-control"}))


class CarSearchForm(forms.Form):
    model = forms.CharField(max_length=255, required=False, label="",
                            widget=forms.TextInput(
                                attrs={"class": "form-control"}))


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label="",
                           widget=forms.TextInput(
                               attrs={"class": "form-control"}))
