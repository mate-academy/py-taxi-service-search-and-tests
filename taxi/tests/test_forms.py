from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class DriverCreationFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new.driver",
            "password1": "Str0ngPass123!",
            "password2": "Str0ngPass123!",
            "first_name": "New",
            "last_name": "Driver",
            "license_number": "NEW12345",
        }

    def test_form_is_valid_with_correct_license_number(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_wrong_license_number(self):
        for license_number in ("NEW1234", "new12345", "NEWD1234", "NE123456"):
            with self.subTest(license_number=license_number):
                self.form_data["license_number"] = license_number
                form = DriverCreationForm(data=self.form_data)
                self.assertFalse(form.is_valid())
                self.assertIn("license_number", form.errors)


class SearchFormTests(TestCase):
    def test_search_forms_allow_empty_value(self):
        for form_class, field in (
                (DriverSearchForm, "username"),
                (CarSearchForm, "model"),
                (ManufacturerSearchForm, "name"),
        ):
            with self.subTest(form=form_class.__name__):
                form = form_class(data={field: ""})
                self.assertTrue(form.is_valid())
