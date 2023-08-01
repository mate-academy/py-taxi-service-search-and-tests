from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    DriverLicenseUpdateForm
)


class DriverFormTest(TestCase):

    def test_invalid_length_of_letters(self):
        form_data = {
            "license_number": "ABCD1234"
        }

        license_form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(license_form.is_valid())

    def test_all_letters_should_be_upper_case(self):
        form_data = {
            "license_number": "Abc12345"
        }

        license_form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(license_form.is_valid())

    def test_invalid_length_of_digits(self):
        form_data = {
            "license_number": "ABC123456"
        }

        license_form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(license_form.is_valid())

    def test_license_number_have_the_5_last_digits(self):
        form_data = {
            "license_number": "ABC1234"
        }

        license_form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(license_form.is_valid())

    def test_valid_license_number(self):
        form_data = {
            "license_number": "ABC12345"
        }

        license_form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(license_form.is_valid())

    def test_create_valid_driver(self):
        form_data = {
            "username": "Test",
            "password1": "test_1234",
            "password2": "test_1234",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "ABC12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_placeholder(self):

        form = DriverSearchForm()
        rendered_html = form.as_p()

        self.assertIn('placeholder="Search by username" ', rendered_html)
