from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Driver


class CarCreationFormTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="TestUser",
            password="password",
            email="1@1.com",
            license_number="AAA11111",
        )
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        self.form_data = {
            "model": "test_model",
            "manufacturer": manufacturer,
            "drivers": Driver.objects.all(),
        }

    def test_car_creation_form_is_valid(self):
        form = CarForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data), list(self.form_data))


class DriverFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "g43tQ3t5",
            "password2": "g43tQ3t5",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        self.test_data = (
            "test", "testtest", "AAAAAAAA", "11111111", "AAAA11111"
        )

    def test_driver_creation_form_is_valid(self):
        self.form_data["license_number"] = "AAA11111"
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_not_valid(self):
        for test_item in self.test_data:
            self.form_data["license_number"] = test_item
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())
            self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_is_valid(self):
        get_user_model().objects.create_user(
            username="test_user",
            password="password",
            email="test@example.com",
            license_number="AAA11111",
        )
        updated_data = {"license_number": "BBB22222"}
        form = DriverLicenseUpdateForm(data=updated_data)
        self.assertEqual(form.data, updated_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_is_not_valid(self):
        get_user_model().objects.create_user(
            username="test_user",
            password="password",
            email="test@example.com",
            license_number="AAA11111",
        )
        for test_item in self.test_data:
            updated_data = {"license_number": test_item}
            form = DriverLicenseUpdateForm(data=updated_data)
            self.assertFalse(form.is_valid())
            self.assertIn("license_number", form.errors)
