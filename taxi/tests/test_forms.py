from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm, validate_license_number
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def test_car_form_valid_data(self):
        user = get_user_model().objects.create_user(username="testuser")
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        form_data = {
            "model": "Test Model",
            "manufacturer": manufacturer.id,
            "drivers": [user.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        form_data = {"model": "", "manufacturer": ""}
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_data(self):
        form_data = {
            "username": "",
            "password1": "",
            "password2": "",
            "license_number": "invalid_license",
            "first_name": "",
            "last_name": "",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_clean_license_number(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12346",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_license_number = form.clean_license_number()
        self.assertEqual(cleaned_license_number, "ABC12346")

    def test_validate_license_number(self):
        valid_license_number = "ABC12345"
        invalid_license_number = "invalid_license"
        self.assertEqual(
            validate_license_number(valid_license_number),
            valid_license_number
        )
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid_data(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_data(self):
        form_data = {"license_number": "invalid_license"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_clean_license_number(self):
        form_data = {"license_number": "ABC12346"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_license_number = form.cleaned_data["license_number"]
        self.assertEqual(cleaned_license_number, "ABC12346")


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid_data(self):
        form_data = {"username": "testuser"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_invalid_data(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_render(self):
        rendered_form = DriverSearchForm().as_p()
        self.assertIn(
            'placeholder="Search by username"', rendered_form
        )


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid_data(self):
        form_data = {"model": "Test Model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_invalid_data(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_render(self):
        rendered_form = CarSearchForm().as_p()
        self.assertIn('placeholder="Search by model"', rendered_form)


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid_data(self):
        form_data = {"name": "Test Manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_invalid_data(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_render(self):
        rendered_form = ManufacturerSearchForm().as_p()
        self.assertIn('placeholder="Search by name"', rendered_form)
