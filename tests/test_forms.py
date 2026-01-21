from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.models import Manufacturer, Car
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)


class FormsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_car_form_is_valid(self):
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Corolla")
        self.assertEqual(form.cleaned_data["manufacturer"], self.manufacturer)
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
        form_data = {"username": "testuser"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_driver_search_form_empty_username_is_valid(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_car_search_form_is_valid(self):
        form_data = {"model": "Corolla"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Corolla")

    def test_car_search_form_empty_model_is_valid(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturer_search_form_is_valid(self):
        form_data = {"name": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")

    def test_manufacturer_search_form_empty_name_is_valid(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_validate_license_number_valid(self):
        valid_license = "ABC12345"
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
