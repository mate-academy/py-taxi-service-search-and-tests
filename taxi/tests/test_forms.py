from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.forms import (DriverLicenseUpdateForm,
                        DriverUsernameSearchForm, CarModelSearchForm,
                        ManufacturerNameSearchForm)
from taxi.models import Car, Manufacturer


class DriverCreationFormTest(TestCase):
    def test_create_driver_with_valid_data(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_driver_creation_invalid_license(self):
        form = DriverLicenseUpdateForm(data={"license_number": "A12"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_too_short(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AB12"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1", password="pass123", license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2", password="pass123", license_number="XYZ67890"
        )

    def test_create_car_with_drivers(self):
        self.client.force_login(self.driver1)

        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }

        self.client.post(reverse("taxi:car-create"), data=form_data)

        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.first()
        self.assertEqual(car.model, "Corolla")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertQuerysetEqual(
            car.drivers.order_by("id"),
            [self.driver1, self.driver2],
            transform=lambda x: x,
        )


class DriverUsernameSearchFormTest(TestCase):
    def test_valid_username_input(self):
        form = DriverUsernameSearchForm(data={"username": "john_doe"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john_doe")

    def test_empty_username_input(self):
        form = DriverUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")


class CarModelSearchFormTest(TestCase):
    def test_valid_model_input(self):
        form = CarModelSearchForm(data={"model": "Tesla Model S"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Tesla Model S")

    def test_empty_model_input(self):
        form = CarModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")


class ManufacturerNameSearchFormTest(TestCase):
    def test_valid_name_input(self):
        form = ManufacturerNameSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")

    def test_empty_name_input(self):
        form = ManufacturerNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
