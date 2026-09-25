from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple
from django.test import SimpleTestCase, TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)


class LicenseNumberValidationTests(SimpleTestCase):
    def assert_invalid(self, *license_numbers):
        for license_number in license_numbers:
            with self.subTest(license_number=license_number):
                with self.assertRaises(ValidationError):
                    validate_license_number(license_number)

    def test_valid_license_number_is_returned(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_must_have_8_characters(self):
        self.assert_invalid("ABC1234", "ABC123456")

    def test_first_3_characters_must_be_uppercase_letters(self):
        self.assert_invalid("abc12345", "AB123456", "1BC12345")

    def test_last_5_characters_must_be_digits(self):
        self.assert_invalid("ABCD2345", "ABC1234X")


class DriverFormsTests(TestCase):
    creation_data = {
        "username": "new.driver",
        "password1": "Str0ng-pass-42",
        "password2": "Str0ng-pass-42",
        "first_name": "New",
        "last_name": "Driver",
        "license_number": "NEW12345",
    }

    def test_creation_form_with_valid_data(self):
        form = DriverCreationForm(data=self.creation_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["license_number"], "NEW12345")
        self.assertEqual(form.cleaned_data["first_name"], "New")
        self.assertEqual(form.cleaned_data["last_name"], "Driver")

    def test_creation_form_validates_license_number(self):
        form = DriverCreationForm(
            data={**self.creation_data, "license_number": "new12345"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_update_form_accepts_valid_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "UPD12345"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_license_update_form_rejects_invalid_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "UPD123"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(SimpleTestCase):
    def test_drivers_are_rendered_as_checkboxes(self):
        self.assertIsInstance(
            CarForm().fields["drivers"].widget, CheckboxSelectMultiple
        )


class SearchFormsTests(SimpleTestCase):
    search_forms = (
        (DriverSearchForm, "username"),
        (CarSearchForm, "model"),
        (ManufacturerSearchForm, "name"),
    )

    def test_search_forms_are_valid_without_query(self):
        for form_class, _ in self.search_forms:
            with self.subTest(form=form_class.__name__):
                self.assertTrue(form_class(data={}).is_valid())

    def test_search_forms_return_the_query(self):
        for form_class, field_name in self.search_forms:
            with self.subTest(form=form_class.__name__):
                form = form_class(data={field_name: "abc"})
                self.assertTrue(form.is_valid())
                self.assertEqual(form.cleaned_data[field_name], "abc")

    def test_search_fields_have_placeholder_instead_of_label(self):
        for form_class, field_name in self.search_forms:
            with self.subTest(form=form_class.__name__):
                field = form_class().fields[field_name]
                self.assertEqual(field.label, "")
                self.assertEqual(
                    field.widget.attrs["placeholder"],
                    f"Search by {field_name}",
                )
