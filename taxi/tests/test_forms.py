from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_with_all_valid_fields(self) -> None:
        form_data = {"username": "test_user",
                     "password1": "test_user_password228",
                     "password2": "test_user_password228",
                     "license_number": "ABD54345",
                     "first_name": "Global",
                     "last_name": "Test"}
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_valid_field(self) -> None:
        form_data = {"license_number": "ABD54345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_format(self) -> None:
        invalid_license_numbers = ["ZYX1234A",
                                   "1ABCD234",
                                   "INVALID",
                                   "11111XYZ",
                                   "X9876543",
                                   "AA11BB22",
                                   "987",
                                   "AAA111",
                                   "XYZZYX",
                                   "X"]
        valid_license_numbers = ["XYZ98765",
                                 "LMN12345",
                                 "PQR67890"]

        for license_number in valid_license_numbers:
            form_data = {"username": "test_user",
                         "password1": "test_user_password228",
                         "password2": "test_user_password228",
                         "license_number": license_number,
                         "first_name": "Global",
                         "last_name": "Test"}
            form = DriverCreationForm(data=form_data)
            self.assertTrue(form.is_valid())

        for license_number in invalid_license_numbers:
            form_data = {"username": "test_user",
                         "password1": "test_user_password228",
                         "password2": "test_user_password228",
                         "license_number": license_number,
                         "first_name": "Global",
                         "last_name": "Test"}
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
