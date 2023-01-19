from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, MaxLengthValidator

from taxi.models import Driver, Car


class DriverForm(UserCreationForm):
    license_number = forms.CharField(
        validators=[
            RegexValidator(
                r"[A-Z]{3}[0-9]{5}",
                "License number should has format XXXDDDDD, where X is "
                "uppercase letter and D is digit"
            )
        ]
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


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


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
