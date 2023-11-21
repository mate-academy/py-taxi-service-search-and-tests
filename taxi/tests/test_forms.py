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
        valid_license_numbers = ["ABD54345",
                                 "ABC43345",
                                 "FTP40441"]
        invalid_license_numbers = ["BA1111AB",
                                   "12fEFA11",
                                   "ASDFJ43",
                                   "AB111111",
                                   "111111AB",
                                   "A9999999",
                                   "11AA11AA",
                                   "234",
                                   "111A",
                                   "OAOAOK",
                                   "NEOK",
                                   "O"]

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
