from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Driver


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save(commit=False)
        self.assertEqual(driver.username, form_data["username"])
        self.assertEqual(driver.first_name, form_data["first_name"])
        self.assertEqual(driver.last_name, form_data["last_name"])
        self.assertEqual(driver.license_number, form_data["license_number"])
