from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LENGTH = 8
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                r"[A-Z]{3}[0-9]{5}",
                "License number should has format XXXDDDDD, where X is "
                "uppercase letter and D is digit"
            ),
            MaxLengthValidator(
                MAX_LENGTH,
                "License number should has 8 character"
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by username",
        })
    )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
