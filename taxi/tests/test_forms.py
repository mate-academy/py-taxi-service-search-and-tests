from django.test import TestCase


from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "1A2g3s4f1234",
            "password2": "1A2g3s4f1234",
            "first_name": "test",
            "last_name": "test",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
