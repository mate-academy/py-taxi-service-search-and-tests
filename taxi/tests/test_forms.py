from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "RED12345"
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_author_creation_form_with_lisense_number_is_valid(self):

        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)

    def test_author_creation_form_with_not_expected_length(self):
        self.form_data["license_number"] = "RED123458"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)

    def test_author_creation_form_with_not_five_digits(self):
        self.form_data["license_number"] = "RED1234U"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)

    def test_author_creation_form_with_not_uppercase_letters(self):
        self.form_data["license_number"] = "red12345"

        self.assertFalse(self.form.is_valid())
        self.assertNotEqual(self.form.cleaned_data, self.form_data)
