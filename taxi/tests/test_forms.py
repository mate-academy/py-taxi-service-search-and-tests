from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTestCase(TestCase):
    def test_car_form(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test_driver12345",
            license_number="NAN21019"
        )
        manufacturer = Manufacturer.objects.create(
            name="Test"
        )
        form_data = {
            "model": "Car Model",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form(self) -> None:
        form_data = {
            "username": "test_driver",
            "password1": "John31Doe",
            "password2": "John31Doe",
            "license_number": "XYZ12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form(self) -> None:
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self) -> None:
        form_data = {
            "username": "test_user",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self) -> None:
        form_data = {
            "searched_model": "Car Model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self) -> None:
        form_data = {
            "searched_name": "Manufacturer 1",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
