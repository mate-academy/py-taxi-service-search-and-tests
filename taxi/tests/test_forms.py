from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_fields_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        user = form.save()
        self.assertTrue(user.check_password(form_data["password1"]))
        self.assertEqual(user.username, form_data["username"])
        self.assertEqual(user.license_number, form_data["license_number"])
