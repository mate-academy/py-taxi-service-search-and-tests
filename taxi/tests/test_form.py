from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsCreationTests(TestCase):
    def test_driver_creation_form_with_additional_options(self):
        form_data = {
            "username": "user1",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "testName",
            "last_name": "testLastName",
            "license_number": "HHH12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_valid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "GGG54321",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "123aaa",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertFalse(form.is_valid())
