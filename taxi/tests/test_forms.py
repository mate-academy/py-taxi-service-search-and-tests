from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class DriverCreationFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345",
        }

    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_invalid_license_is_not_valid(self):
        self.form_data["license_number"] = "tst12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    @staticmethod
    def create_form(license_number: str) -> DriverLicenseUpdateForm:
        return DriverLicenseUpdateForm(
            data={"license_number": license_number}
        )

    def test_valid_license_number(self):
        self.assertTrue(self.create_form("TST12345").is_valid())

    def test_license_number_should_consist_of_8_characters(self):
        for license_number in ("TST1234", "TST123456"):
            with self.subTest(license_number=license_number):
                form = self.create_form(license_number)
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors["license_number"],
                    ["License number should consist of 8 characters"],
                )

    def test_first_3_characters_should_be_uppercase_letters(self):
        for license_number in ("tst12345", "TsT12345", "T1T12345"):
            with self.subTest(license_number=license_number):
                form = self.create_form(license_number)
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors["license_number"],
                    ["First 3 characters should be uppercase letters"],
                )

    def test_last_5_characters_should_be_digits(self):
        for license_number in ("TST1234A", "TSTABCDE"):
            with self.subTest(license_number=license_number):
                form = self.create_form(license_number)
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors["license_number"],
                    ["Last 5 characters should be digits"],
                )


class SearchFormsTests(TestCase):
    def test_search_forms_are_valid_with_search_value(self):
        forms = (
            DriverSearchForm(data={"username": "test"}),
            CarSearchForm(data={"model": "test"}),
            ManufacturerSearchForm(data={"name": "test"}),
        )
        for form in forms:
            with self.subTest(form=type(form).__name__):
                self.assertTrue(form.is_valid())

    def test_search_forms_are_valid_without_search_value(self):
        for form_class in (
            DriverSearchForm,
            CarSearchForm,
            ManufacturerSearchForm,
        ):
            with self.subTest(form=form_class.__name__):
                self.assertTrue(form_class(data={}).is_valid())

    def test_search_fields_placeholders(self):
        placeholders = (
            (DriverSearchForm, "username", "Search by username"),
            (CarSearchForm, "model", "Search by model"),
            (ManufacturerSearchForm, "name", "Search by name"),
        )
        for form_class, field, placeholder in placeholders:
            with self.subTest(form=form_class.__name__):
                widget = form_class().fields[field].widget
                self.assertEqual(widget.attrs["placeholder"], placeholder)
