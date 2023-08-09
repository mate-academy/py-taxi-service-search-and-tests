from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):

    def test_driver_creation_form_license_number_first_name_last_name(self):
        form_data = {
            "username": "new_user",
            "first_name": "Test",
            "last_name": "last",
        }

        form = DriverCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)

        self.assertDictEqual(form.cleaned_data, form_data)
