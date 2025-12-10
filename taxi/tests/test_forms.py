from django.test import TestCase
from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_author_creation_form_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "Testuser123!",
            "password2": "Testuser123!",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ADM56984",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()

        self.assertEqual(driver.username, form_data["username"])
        self.assertEqual(driver.first_name, form_data["first_name"])
        self.assertEqual(driver.last_name, form_data["last_name"])
        self.assertEqual(driver.license_number, form_data["license_number"])
        self.assertTrue(driver.check_password(form_data["password1"]))
