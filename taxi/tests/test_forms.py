from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    ManufacturerSearchForm,
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm
)
from taxi.models import Manufacturer


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_is_valid(self):
        form_data = {
            "name": "Ford",
        }
        manufacturer_search_form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(manufacturer_search_form.is_valid())
        self.assertEqual(manufacturer_search_form.cleaned_data, form_data)


class CarFormTest(TestCase):
    def test_car_form_is_valid(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
            password="test1234abta",
            license_number="ABC12345",
            first_name="Bob",
            last_name="Smith",
        )
        manufacturer = Manufacturer.objects.create(
            name="Fiat",
            country="Italy"
        )
        form_data = {
            "model": "QWER",
            "manufacturer": manufacturer,
            "drivers": [driver],
        }
        car_form = CarForm(data=form_data)

        self.assertTrue(car_form.is_valid())
        self.assertEqual(list(car_form.cleaned_data), list(form_data))


class DriverCreationFormTest(TestCase):
    def test_driver_creation(self):
        form_data = {
            "username": "test_user",
            "password1": "test1234abstrac",
            "password2": "test1234abstrac",
            "first_name": "Bob",
            "license_number": "ABC12345",
            "last_name": "Smith",
        }
        driver_form = DriverCreationForm(data=form_data)

        self.assertTrue(driver_form.is_valid())
        self.assertEqual(driver_form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update(self):

        self.assertFalse(
            DriverLicenseUpdateForm(
                data={"license_number": "ABCD1234123"}
            ).is_valid(),
            msg="License number must be of length 8"
        )
        self.assertFalse(
            DriverLicenseUpdateForm(
                data={"license_number": "ABC1234"}
            ).is_valid(),
            msg="Last 5 characters of license number must be digits"
        )
        self.assertFalse(
            DriverLicenseUpdateForm(
                data={"license_number": "ABc12345"}
            ).is_valid(),
            msg="First 3 characters of license number must be upper letters"
        )

        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            msg="Returns True if correct license number"
        )
        self.assertEqual(
            form.cleaned_data, form_data
        )


class DriverSearchFormTest(TestCase):
    def test_driver_search(self):
        form_data = {"username": "test_user"}
        form = DriverSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
