from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from taxi.models import Car, Driver


class CarCreateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class LicenseValidatorMixin(forms.ModelForm):
    FIRST_CHARS_NUMBER = 3
    LAST_CHARS_NUMBER = 5

    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                regex="^[A-Z]{" + str(FIRST_CHARS_NUMBER) + "}",
                message=f"The first {FIRST_CHARS_NUMBER} characters of the "
                f"license number must be uppercase letters!"
            ),
            RegexValidator(
                regex=r"^\D*(\d{" + str(LAST_CHARS_NUMBER) + "})$",
                message=f"Last {LAST_CHARS_NUMBER} characters must be digits!",
            ),
        ]
    )


class DriverCreationForm(LicenseValidatorMixin):
    MIN_USERNAME_LENGTH = 3

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "password",
            "first_name",
            "last_name",
            "email",
            "license_number",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < DriverCreationForm.MIN_USERNAME_LENGTH:
            raise forms.ValidationError(
                f"Username is too short. Min. length is "
                f"{DriverCreationForm.MIN_USERNAME_LENGTH} symbols."
            )
        return username


class DriverLicenseUpdateForm(LicenseValidatorMixin):

    class Meta:
        model = Driver
        fields = ["license_number"]


class ListSearchForm(forms.Form):

    search_data = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput()
    )

    def __init__(self, *args, placeholder="Search", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search_data"].widget.attrs["placeholder"] = placeholder
