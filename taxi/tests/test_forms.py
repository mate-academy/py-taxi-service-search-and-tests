from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Car, Driver, Manufacturer


class FormTests(TestCase):

    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(car.model, "Corolla")
        self.assertIn(self.driver, car.drivers.all())

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "new_driver",
            "password1": "password1234",
            "password2": "password1234",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "invalid"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "DEF67890"}
        form = DriverLicenseUpdateForm(instance=self.driver, data=form_data)
        self.assertTrue(form.is_valid())
        updated_driver = form.save()
        self.assertEqual(updated_driver.license_number, "DEF67890")

    def test_driver_license_update_form_invalid(self):
        form_data = {"license_number": "12345"}
        form = DriverLicenseUpdateForm(instance=self.driver, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_search_form(self):
        form_data = {"username": "testdriver"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testdriver")

    def test_car_search_form(self):
        form_data = {"model": "Camry"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Camry")

    def test_manufacturer_search_form(self):
        form_data = {"model": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Toyota")
