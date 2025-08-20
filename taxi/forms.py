from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car
from taxi.validators import validate_license_number


User = get_user_model()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarModelSearchForm(forms.Form):
    model = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Model"}),
    )


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):  # this logic is optional, but possible
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["license_number"]

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )


class ManufacturerNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
    )
