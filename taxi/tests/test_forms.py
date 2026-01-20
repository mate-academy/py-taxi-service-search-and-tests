from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Driver, Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)

PASSWORD = "#0;8{P0>EVjY"


class FormTestSetupMixin:
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password=PASSWORD
        )
        self.client.force_login(self.user)


class CarFormTest(FormTestSetupMixin, TestCase):
    def test_car_form_empty_drivers(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        form = CarForm(
            data={
                "model": "Test Model",
                "manufacturer": manufacturer.id,
                "drivers": [],
            }
        )
        self.assertFalse(form.is_valid())

    def test_car_form_no_data(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(FormTestSetupMixin, TestCase):
    def test_driver_creation_form_valid_data(self):
        form = DriverCreationForm(
            data={
                "username": "testdriver",
                "password1": PASSWORD,
                "password2": PASSWORD,
                "license_number": "ABC12345",
                "first_name": "Test",
                "last_name": "Driver",
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "testdriver",
                "password1": PASSWORD,
                "password2": PASSWORD,
                "license_number": "12345",
                "first_name": "Test",
                "last_name": "Driver",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(FormTestSetupMixin, TestCase):
    def test_driver_license_update_form_valid_data(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password=PASSWORD,
            license_number="ABC12345",
        )
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF67890"}, instance=driver
        )
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_license_number(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password=PASSWORD,
            license_number="ABC12345",
        )
        form = DriverLicenseUpdateForm(
            data={"license_number": "12345"}, instance=driver
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverSearchFormTest(FormTestSetupMixin, TestCase):
    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"username": "testdriver"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_no_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())


class CarSearchFormTest(FormTestSetupMixin, TestCase):
    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_no_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(FormTestSetupMixin, TestCase):
    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_no_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
