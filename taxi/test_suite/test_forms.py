from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver
from django.contrib.auth import get_user_model


User = get_user_model()


class DriverFormsTest(TestCase):
    def test_driver_creation_form_valid(self):
        data = {
            "username": "ivan",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
            "license_number": "TES12345",
            "first_name": "Ivan",
            "last_name": "Ivanov"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        data = {
            "username": "ivan",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
            "license_number": "WRONG123",
            "first_name": "Ivan",
            "last_name": "Ivanov"
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid(self):
        driver = Driver.objects.create(username="ivan",
                                       license_number="TES12345")
        data = {"license_number": "ABC54321"}
        form = DriverLicenseUpdateForm(instance=driver, data=data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        driver = Driver.objects.create(username="ivan",
                                       license_number="TES12345")
        data = {"license_number": "WRONG123"}
        form = DriverLicenseUpdateForm(instance=driver, data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
