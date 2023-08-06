from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def setUp(self):
        self.driver_form_data = {
            "username": "test_user",
            "password1": "driver123",
            "password2": "driver123",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12346"}

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.driver_form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.driver_form_data)

    def test_driver_license_update_form(self):
        data = {"license_number": "ABC1239"}
        form = DriverLicenseUpdateForm(data=data)

        self.assertTrue(form.clean_license_number)
        self.assertEqual(form.data, data)
