from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_licence_num(self):
        form_data = {
            "username": "testuser",
            "password1": "Testpass123",
            "password2": "Testpass123",
            "first_name": "jack test",
            "last_name": "black test",
            "license_number": "JAK12312",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
