from django.test import TestCase

from taxi.forms import (
    SearchForm,
    CarForm,
    DriverLicenseUpdateForm,
    DriverCreationForm,
)


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.form = SearchForm()

    def test_search_form_has_search_criteria_field(self):
        self.assertIn("search_criteria", self.form.fields)


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.form = CarForm()

    def test_search_form_has_search_criteria_field(self):
        self.assertIn("drivers", self.form.fields)


class DriverCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.form = DriverCreationForm()

    def test_form_has_additional_fields(self):
        """
        Test that form contains additional fields:
            1. license_number
            2. first_name
            3. last_name
        """
        self.assertIn("license_number", self.form.Meta.fields)
        self.assertIn("first_name", self.form.Meta.fields)
        self.assertIn("last_name", self.form.Meta.fields)

    def test_cleaned_license_number(self):
        self.form = DriverLicenseUpdateForm(
            data={"license_number": "MVT12345"}
        )

        self.assertTrue(self.form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.form = DriverLicenseUpdateForm()

    def test_driver_update_form_has_one_field(self):
        """Test that form contains only 'license_number' field"""
        self.assertEqual(len(self.form.fields), 1)

        form_fields = list(self.form.fields.keys())
        self.assertEqual(form_fields, ["license_number"])

    def test_cleaned_license_number(self):
        self.form = DriverLicenseUpdateForm(
            data={"license_number": "MVT12345"}
        )

        self.assertTrue(self.form.is_valid())
