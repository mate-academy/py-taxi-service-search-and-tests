from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test_username",
            password="strong_password"
        )
        self.form_data = {
            "username": "King_of_the_tests",
            "password1": "secret_password1984#",
            "password2": "secret_password1984#",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "license_number": "TNT54321",
        }

    def test_user_creation_with_customs_fields(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)