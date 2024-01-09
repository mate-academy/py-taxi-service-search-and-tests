from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverFormTests(TestCase):

    def setUp(self):
        self.form_data = {
            "username": "new_username",
            "password1": "user12test",
            "password2": "user12test",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_creation_validation(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_update_validation(self):
        form_data = {
            "license_number": "ABC12346",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
