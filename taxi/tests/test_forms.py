from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Driver


class DriverCreationFormTests(TestCase):
    def make_form(self, license_number):
        return DriverCreationForm(
            data={
                "username": "newdriver",
                "password1": "Strong-password-123",
                "password2": "Strong-password-123",
                "license_number": license_number,
                "first_name": "New",
                "last_name": "Driver",
            }
        )

    def test_valid_license_number_is_accepted(self):
        self.assertTrue(self.make_form("ABC12345").is_valid())

    def test_invalid_license_numbers_are_rejected(self):
        for license_number in ("ABC1234", "abc12345", "ABC12A45"):
            with self.subTest(license_number=license_number):
                form = self.make_form(license_number)

                self.assertFalse(form.is_valid())
                self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license_number_is_accepted(self):
        driver = Driver.objects.create_user(
            username="driver",
            password="Strong-password-123",
            license_number="DEF12345",
        )
        form = DriverLicenseUpdateForm(
            instance=driver,
            data={"license_number": "ABC12345"},
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")


class SearchFormTests(TestCase):
    def test_search_forms_accept_an_empty_query(self):
        for form_class in (
            ManufacturerSearchForm,
            CarSearchForm,
            DriverSearchForm,
        ):
            with self.subTest(form=form_class.__name__):
                self.assertTrue(form_class(data={}).is_valid())
