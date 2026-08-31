from django.contrib.auth.forms import UserCreationForm
from django import forms
from taxi.models import Driver, Car

class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number", "first_name", "last_name",)

class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
