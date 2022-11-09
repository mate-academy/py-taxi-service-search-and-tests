from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test",
            "password1": "123test123",
            "password2": "123test123",
            "first_name": "first",
            "last_name": "last",
        }

    def test_driver_creation_form_is_valid_with_added_fields(self):
        self.form_data.update({"license_number": "AAA12345"})

        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_license_number_validation(self):
        incorrect_licence_numbers = [
            "aaaa1234",
            "aaa1234",
            "AA123456",
            "9" * 9,
            "7" * 7
        ]

        for iln in incorrect_licence_numbers:
            with self.subTest(amount=iln):
                self.form_data.update({"license_number": iln})

                form = DriverCreationForm(data=self.form_data)

                self.assertFalse(form.is_valid())
