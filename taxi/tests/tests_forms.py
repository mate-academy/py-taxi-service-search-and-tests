from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        validate_license_number)
from taxi.models import Driver


class FormsTests(TestCase):
    def test_driver_creation_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "driver12test",
            "password2": "driver12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA11111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license_number_with_validation(self):
        driver = get_user_model().objects.create_user(
            username="new_user",
            password="driver12test",
            first_name="Test first",
            last_name="Test last",
            license_number="AAA11111"
        )
        form_data = {
            "license_number": "AAA11112",
        }
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        form.save()
        self.assertTrue(form.is_valid)
        driver = Driver.objects.get(pk=1)
        self.assertEqual(driver.license_number, form_data["license_number"])
        form_data = {"license_number": "AAA1111", }
        with self.assertRaises(ValueError):
            DriverLicenseUpdateForm(data=form_data, instance=driver).save()
        form_data = {"license_number": "aaa11111", }
        with self.assertRaises(ValueError):
            DriverLicenseUpdateForm(data=form_data, instance=driver).save()
        form_data = {"license_number": "AA111111", }
        with self.assertRaises(ValueError):
            DriverLicenseUpdateForm(data=form_data, instance=driver).save()
        form_data = {"license_number": "TEST1111", }
        with self.assertRaises(ValueError):
            DriverLicenseUpdateForm(data=form_data, instance=driver).save()

    def test_validate_license_number(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("AAA1111")
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("aaa11111")
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("AA111111")
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            validate_license_number("TEST1111")
