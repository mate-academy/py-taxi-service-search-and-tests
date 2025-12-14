from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriversSearchForm)


class FormsTests(TestCase):
    def test_driver_creation_form_with_username_first_last_name_is_valid(self):
        form_data = {
            "username": "Driver",
            "password1": "driver45634d",
            "password2": "driver45634d",
            "license_number": "MOP23456",
            "first_name": "test_first",
            "last_name": "test_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_valid_license_update(self):
        driver = get_user_model().objects.create_user(
            username="driver123",
            license_number="POL39455",
            password="<PASSWORD1>")
        form_data = {"license_number": "SKD39576"}
        form = DriverLicenseUpdateForm(instance=driver, data=form_data)
        self.assertTrue(form.is_valid())
