from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_licence_first_last_name_is_valid(self):

        form_data = {
            "username": "tester",
            "password1": "parol123",
            "password2": "parol123",
            "first_name": "Joe",
            "last_name": "Shmoe",
            "license_number": "AAA11111",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
