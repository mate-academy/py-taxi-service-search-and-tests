from django.test import TestCase

from taxi.forms import DriverSearchForm, DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "user2",
            "password1": "newtest2",
            "password2": "newtest2",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )


class DriverSearchFormTests(TestCase):
    def test_form_validation(self):
        form = DriverSearchForm({"username": "Driver3"})
        self.assertTrue(form.is_valid())

    def test_no_query_validation(self):
        form = DriverSearchForm({"username": ""})
        self.assertTrue(form.is_valid())
