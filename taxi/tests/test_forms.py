from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_licence_number_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test123user!",
            "password2": "test123user!",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "BDR12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertEqual(form.errors, {})
        driver = form.save()
        self.assertEqual(driver.username, "new_user")
        self.assertEqual(driver.first_name, "Test first")
        self.assertEqual(driver.license_number, "BDR12345")
