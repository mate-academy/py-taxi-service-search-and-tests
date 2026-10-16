from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class DriverCreationFormTests(TestCase):
    def _form_data(self, license_number):
        return {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test",
            "last_name": "User",
            "license_number": license_number,
        }

    def test_valid_license_number(self):
        form = DriverCreationForm(data=self._form_data("ABC12345"))
        self.assertTrue(form.is_valid())

    def test_license_too_short(self):
        form = DriverCreationForm(data=self._form_data("ABC123"))
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_too_long(self):
        form = DriverCreationForm(data=self._form_data("ABC123456"))
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_first_three_not_uppercase_letters(self):
        form = DriverCreationForm(data=self._form_data("abc12345"))
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_last_five_not_digits(self):
        form = DriverCreationForm(data=self._form_data("ABC12E45"))
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ98765"})
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "123"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormTests(TestCase):
    def test_search_forms_are_not_required(self):
        self.assertTrue(DriverSearchForm(data={}).is_valid())
        self.assertTrue(CarSearchForm(data={}).is_valid())
        self.assertTrue(ManufacturerSearchForm(data={}).is_valid())

    def test_search_forms_accept_value(self):
        self.assertTrue(DriverSearchForm(data={"username": "abc"}).is_valid())
        self.assertTrue(CarSearchForm(data={"model": "abc"}).is_valid())
        self.assertTrue(
            ManufacturerSearchForm(data={"name": "abc"}).is_valid()
        )
