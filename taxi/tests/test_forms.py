from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class CreateDriverFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "user11test",
            "password2": "user11test",
            "first_name": "first_test",
            "last_name": "last_test",
        }

    def test_driver_creation_form_with_valid_license(self):
        self.form_data["license_number"] = "ABC12345"
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_invalid_license(self):
        for license_number in ["abc12345", "ABCDEFGH", "ABC1234"]:
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)

            self.assertFalse(form.is_valid())

    def test_driver_creation_form_without_license(self):
        form = DriverCreationForm(self.form_data)

        self.assertFalse(form.is_valid())


class UpdateDriverFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "user11test",
            "password2": "user11test",
            "first_name": "first_test",
            "last_name": "last_test",
            "license_number": "ABC12345"
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_update_form_with_valid_license(self):
        self.form = DriverLicenseUpdateForm(
            data={"license_number": "EFG56789"}
        )

        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data["license_number"], "EFG56789")

    def test_update_form_with_invalid_license(self):
        for license_number in ["abc12345", "ABCDEFGH", "ABC1234"]:
            self.form = DriverCreationForm(
                data={"license_number": license_number}
            )

            self.assertFalse(self.form.is_valid())
            self.assertNotIn("license_number", self.form.cleaned_data)
            self.assertEqual(self.form.data["license_number"], license_number)

    def test_update_form_without_license(self):
        self.form = DriverLicenseUpdateForm(
            data={"license_number": ""}
        )

        self.assertFalse(self.form.is_valid())
        self.assertNotIn("license_number", self.form.cleaned_data)
        self.assertEqual(self.form.data["license_number"], "")


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.form = CarSearchForm()

    def test_model_field_placeholder(self):
        self.assertEqual(
            self.form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_model_field_not_required(self):
        self.assertFalse(self.form.fields["model"].required)


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.form = DriverSearchForm()

    def test_model_field_placeholder(self):
        self.assertEqual(
            self.form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )

    def test_model_field_not_required(self):
        self.assertFalse(self.form.fields["username"].required)


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.form = ManufacturerSearchForm()

    def test_model_field_placeholder(self):
        self.assertEqual(
            self.form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )

    def test_model_field_not_required(self):
        self.assertFalse(self.form.fields["name"].required)
