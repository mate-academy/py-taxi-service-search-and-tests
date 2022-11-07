from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    license_number = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "license_number", "password1", "password2")
