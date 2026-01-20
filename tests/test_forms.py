from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    validate_license_number
)
from taxi.models import Car, Manufacturer


class FormsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestDummy",
            password="testpass123",
            license_number="SOS322223"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="BWD",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="UAZ Factory",
            country="Muchosransk"
        )
        self.car1 = Car.objects.create(
            model="Panzerhaubitze 2000",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="UAZ",
            manufacturer=self.manufacturer2
        )

    def test_car_form_is_valid(self):
        form_data = {
            "model": "Panzerhaubitze 2000",
            "manufacturer": self.manufacturer1.id,
            "drivers": [self.user.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Panzerhaubitze 2000")
        self.assertEqual(form.cleaned_data["manufacturer"], self.manufacturer1)
        self.assertEqual(list(form.cleaned_data["drivers"]), [self.user])

    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "driver12test",
            "password2": "driver12test",
            "license_number": "DEF67890",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "newdriver")
        self.assertEqual(form.cleaned_data["license_number"], "DEF67890")

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "driver12test",
            "password2": "driver12test",
            "license_number": "invalid",
            "first_name": "First",
            "last_name": "Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_is_valid(self):
        form_data = {"license_number": "XYZ12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "XYZ12345")

    def test_driver_license_update_form_invalid_license_number(self):
        form_data = {"license_number": "invalid"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_search_form_is_valid(self):
        form_data = {"username": "TestDummy"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "TestDummy")

    def test_driver_search_form_empty_username_is_valid(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_manufacturer_search_form_is_valid(self):
        form_data = {"name": "BWD"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "BWD")

    def test_manufacturer_search_form_empty_name_is_valid(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_validate_license_number_valid(self):
        valid_license = "SOS32222"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_validate_license_number_invalid_length(self):
        invalid_license = "ABC1234"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license)

    def test_validate_license_number_invalid_first_part(self):
        invalid_license = "AB123456"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license)

    def test_validate_license_number_invalid_last_part(self):
        invalid_license = "ABC1234A"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license)
