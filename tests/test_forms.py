from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "driver1",
            "password1": "3tktybqVtrcbrfytwm",
            "password2": "3tktybqVtrcbrfytwm",
            "first_name": "Katya",
            "last_name": "Shyshka",
            "license_number": "KJK23457"
        }

    def test_driver_creation_form_with_fields_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
