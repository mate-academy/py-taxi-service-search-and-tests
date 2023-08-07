from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "black_adam",
            "password1": "iron_black123",
            "password2": "iron_black123",
            "first_name": "adam",
            "last_name": "black",
            "license_number": "BHD65897"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_license_number_contains_eight_characters(self):
        license_number = {"license_number": "DFR1234557"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())

    def test_license_number_contains_three_letter(self):
        license_number = {"license_number": "cas12345"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())

    def test_license_number_contains_five_digits(self):
        license_number = {"license_number": "ASD587cd"}
        form = DriverLicenseUpdateForm(license_number)
        self.assertFalse(form.is_valid())
