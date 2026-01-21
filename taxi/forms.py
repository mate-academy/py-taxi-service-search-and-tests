import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Car

UserModel = get_user_model()


def validate_license_number(value):
    """Valida: 3 letras maiúsculas + 5 dígitos (ex: ABC12345)."""
    if not re.match(r"^[A-Z]{3}\d{5}$", value):
        raise ValidationError(
            "O número da licença deve conter 3 letras maiúsculas seguidas "
            "por 5 dígitos (ex: ABC12345)."
        )


class DriverCreationForm(UserCreationForm):
    """Formulário de criação de usuário/motorista com license_number."""
    license_number = forms.CharField(
        max_length=8,
        required=False,
        validators=[validate_license_number],
        help_text="Formato: ABC12345 (3 letras + 5 dígitos)",
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ("license_number",)


class DriverLicenseUpdateForm(forms.ModelForm):
    """Form para atualizar apenas o número da licença."""
    class Meta:
        model = UserModel
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number", "")
        if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
            raise ValidationError(
                "O número da licença deve conter 3 letras maiúsculas seguidas "
                "por 5 dígitos (ex: ABC12345)."
            )
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
