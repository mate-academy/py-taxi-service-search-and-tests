from django.test import TestCase

from ..forms import (
    DriverLicenseUpdateForm,
    SearchForm,
    DriverCreationForm
)


class TestForms(TestCase):
    def setUp(self):
        self.test_driver_form = DriverCreationForm()
        self.test_search_form = SearchForm()

    def test_driver_creation_form_contains_expected_fields(self):
        expected_fields = ["license_number", "first_name", "last_name"]
        for field in expected_fields:
            self.assertIn(field, self.test_driver_form.fields)

    def test_search_form_field_max_length(self):
        self.assertEqual(self.test_search_form.fields["search_query"].max_length, 50)

    def test_search_form_contains_expected_field(self):
        expected_fields = {"search_query", }
        self.assertEqual(expected_fields, set(self.test_search_form.fields))

    def test_search_form_valid(self):
        form = SearchForm(
            {"search_query": "another",}
        )
        self.assertTrue(form.is_valid())

    def test_search_form_invalid(self):
            form = SearchForm(
                {"search_query": "4"*51 }
            )
            self.assertFalse(form.is_valid())