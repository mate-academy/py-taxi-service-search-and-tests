from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_all_data_is_valid(self):
        form_data = {
            "username": "test1",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_no_data(self):
        form = DriverCreationForm(data={})
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_invalid_data(self):
        form_data = {
            "username": "test" * 200,
            "password1": "1234",
            "password2": "1245",
            "license_number": "CBa12"
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
