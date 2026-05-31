from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):

    def test_driver_creation_form_with_all_data_fields_valid(self):
        form_data = {
            "username": "LeBronnnieJames",
            "password1": "Lbj12345_king",
            "password2": "Lbj12345_king",
            "first_name": "Lebron",
            "last_name": "James",
            "license_number": "LBJ12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
