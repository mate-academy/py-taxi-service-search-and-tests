from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "jim.hopper",
            "password1": "bobo765",
            "license_number": "JIM26531",
            "password2": "bobo765",
            "first_name": "Jim",
            "last_name": "Hopper",
        }

    def test_driver_creation_(self):
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
