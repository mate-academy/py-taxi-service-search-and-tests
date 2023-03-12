from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "jim.hopper",
            "password1": "bobo7657",
            "password2": "bobo7657",
            "first_name": "Jim",
            "last_name": "Hopper",
            "license_number": "JIM26531",
        }

    def test_driver_creation_(self) -> None:
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_license_update_form(self) -> None:
        self.form_data = {
            "license_number": "UTY89424",
        }
        form = DriverLicenseUpdateForm(data=self.form_data,)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data, self.form_data,
        )

    def test_invalid_driver_license_update_form(self) -> None:
        self.form_data = {
            "license_number": "uTy89424",
        }
        form = DriverLicenseUpdateForm(data=self.form_data,)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(
            form.cleaned_data, self.form_data,
        )
