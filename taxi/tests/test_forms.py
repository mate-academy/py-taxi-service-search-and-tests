from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreateAndUpdateFormTest(TestCase):
    def setUp(self):
        self.creation_form_data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "ABC12345"
        }

        self.update_form_data = {
            "license_number": "ABC12345"
        }

    def test_forms_are_valid(self):
        for form, data in (
                (DriverCreationForm, self.creation_form_data),
                (DriverLicenseUpdateForm, self.update_form_data)
        ):
            with self.subTest(form=form):
                actual_form = form(data=data)
                self.assertTrue(actual_form.is_valid())
                self.assertEqual(
                    actual_form.cleaned_data,
                    data
                )

    def test_forms_are_not_valid(self):
        for wrong_license_number in (
                "ABC1234",
                "ABC123456",
                "abc12345",
                "ABCD1234"
        ):
            with self.subTest(license_number=wrong_license_number):
                self.creation_form_data[
                    "license_number"
                ] = wrong_license_number
                self.update_form_data[
                    "license_number"
                ] = wrong_license_number

                self.assertFalse(DriverCreationForm(
                    data=self.creation_form_data).is_valid())

                self.assertFalse(DriverLicenseUpdateForm(
                    data=self.update_form_data).is_valid())
