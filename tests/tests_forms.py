from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm

form_data_valid = {
    "username": "vasya.pupkin",
    "license_number": "ABC12345",
    "first_name": "Vasya",
    "last_name": "Pupkin",
    "password1": "345ert345",
    "password2": "345ert345",
}
form_data_invalid = {
    "username": "dfghgh",
    "license_number": "ABC12345",
    "first_name": "dfgh",
    "last_name": "dfghhgh",
    "password1": "345ertt345",
    "password2": "345",
}


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_is_valid(self) -> None:
        form = DriverCreationForm(data=form_data_valid)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data_valid)

    def test_driver_creation_form_is_invalid(self) -> None:
        form = DriverCreationForm(data=form_data_invalid)
        self.assertFalse(form.is_valid())


class DriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(form_data_valid)
        self.client.force_login(self.driver)

    def test_create_user(self) -> None:
        self.client.post(reverse("taxi:driver-create"), data=form_data_valid)
        new_user = get_user_model().objects.get(
            username=form_data_valid["username"]
        )

        self.assertEqual(
            new_user.first_name, form_data_valid["first_name"]
        )
        self.assertEqual(
            new_user.last_name, form_data_valid["last_name"]
        )
        self.assertEqual(
            new_user.license_number, form_data_valid["license_number"]
        )


class LicenseTests(TestCase):
    def test_update_license_form_is_valid(self):
        license_form = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=license_form)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, license_form)

    def test_update_license_form_first_3_letter(self):
        license_form = {"license_number": "A9812345"}
        form = DriverLicenseUpdateForm(data=license_form)
        self.assertFalse(form.is_valid())

    def test_update_license_form_first_3_upper(self):
        license_form = {"license_number": "Abc12345"}
        form = DriverLicenseUpdateForm(data=license_form)
        self.assertFalse(form.is_valid())

    def test_update_license_form_last_5_digits(self):
        license_form = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=license_form)
        self.assertFalse(form.is_valid())

    def test_update_license_form_8_chars(self):
        license_form = {"license_number": "ABC12345678"}
        form = DriverLicenseUpdateForm(data=license_form)
        self.assertFalse(form.is_valid())
