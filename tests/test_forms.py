from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creating_with_additional_inf(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234@",
            "password2": "user1234@",
            "license_number": "QWE12345",
            "first_name": "UserF",
            "last_name": "UserL",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_validation_driver_create_license_num_len(self):

        form_data = {
            "username": "test_user",
            "password": "test1234@",
            "license_number": "QWE123456"
        }

        form = DriverCreationForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )
