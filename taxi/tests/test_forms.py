from parameterized import parameterized
from django.test import TestCase

from taxi.forms import DriverCreationForm, SearchForm


class TestDriverCreationForm(TestCase):
    def test_fields_driver_creation_form(self):
        form = DriverCreationForm()
        self.assertTrue(
            form.fields["license_number"]
            and form.fields["first_name"]
            and form.fields["last_name"]
        )

    @parameterized.expand(
        [
            (
                "license_number_len",
                {
                    "license_number": "ABC",
                    "username": "test_username",
                    "password1": "test_password",
                    "password2": "test_password",
                },
                False,
            ),
            (
                "license_number_upper",
                {
                    "license_number": "abc12345",
                    "username": "test_username",
                    "password1": "test_password",
                    "password2": "test_password",
                },
                False,
            ),
            (
                "license_number_numbers",
                {
                    "license_number": "abc1234a",
                    "username": "test_username",
                    "password1": "test_password",
                    "password2": "test_password",
                },
                False,
            ),
            (
                "license_number_all_valid",
                {
                    "license_number": "ABC12345",
                    "username": "test_username",
                    "password1": "test_password",
                    "password2": "test_password",
                },
                True,
            ),
        ]
    )
    def test_validate_license(self, name, form_data, expected_bool):
        form = DriverCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), expected_bool)


class TestSearchForm(TestCase):
    def test_search_placeholder(self):
        form = SearchForm("test")
        self.assertEqual(
            form.fields["search_edit"].widget.attrs["placeholder"], "Search by test..."
        )
