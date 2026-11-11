from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class DriverCreationFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "new_user",
            "password1": "User12345test",
            "password2": "User12345test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }

    def test_form_with_valid_data(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_form_rejects_invalid_license_number(self) -> None:
        self.form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_form_rejects_different_passwords(self) -> None:
        self.form_data["password2"] = "Other12345test"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_number_validation(self) -> None:
        cases = {
            "ABC12345": True,
            "ABC1234": False,
            "ABC123456": False,
            "AB123456": False,
            "abc12345": False,
            "ABCD2345": False,
        }
        for license_number, expected in cases.items():
            with self.subTest(license_number=license_number):
                form = DriverLicenseUpdateForm(
                    data={"license_number": license_number}
                )
                self.assertEqual(form.is_valid(), expected)


class SearchFormTests(TestCase):
    def test_search_forms_are_valid_when_empty(self) -> None:
        cases = (
            (DriverSearchForm, "username"),
            (CarSearchForm, "model"),
            (ManufacturerSearchForm, "name"),
        )
        for form_class, field in cases:
            with self.subTest(form=form_class.__name__):
                form = form_class(data={field: ""})
                self.assertTrue(form.is_valid())
                self.assertEqual(form.cleaned_data[field], "")

    def test_driver_search_form_keeps_username(self) -> None:
        form = DriverSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john")

    def test_car_search_form_keeps_model(self) -> None:
        form = CarSearchForm(data={"model": "X5"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "X5")

    def test_manufacturer_search_form_keeps_name(self) -> None:
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "BMW")

    def test_search_forms_reject_too_long_value(self) -> None:
        too_long = "a" * 256
        self.assertFalse(
            DriverSearchForm(data={"username": too_long}).is_valid()
        )
        self.assertFalse(CarSearchForm(data={"model": too_long}).is_valid())
        self.assertFalse(
            ManufacturerSearchForm(data={"name": too_long}).is_valid()
        )

    def test_search_forms_have_placeholders(self) -> None:
        widget = DriverSearchForm().fields["username"].widget
        self.assertEqual(
            widget.attrs["placeholder"],
            "Search by username",
        )
