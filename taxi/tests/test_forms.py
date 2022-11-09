from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class TestDriverCreationForm(TestCase):

    def test_creation_driver(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "BHJ12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

        driver = Driver.objects.create_user(username="test", password="test12345", first_name="first_name",
                                            last_name="last_name", license_number="BHJ12345",)
        driver.refresh_from_db()

        self.assertEqual(driver.username, form_data["username"])

    def test_driver_license_update_form(self):
        form_data = {"license_number": "NJK12345"}

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
