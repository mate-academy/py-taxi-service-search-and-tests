from unittest import TestCase

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from taxi.forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver


class DriverCreateTest(TestCase):

    def test_create_driver_with_valid_license(self):
        form = DriverCreationForm(
            data={
                "license_number": "ADM56586",
                "username": "test__username",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "first_name": "test2",
                "last_name": "test2",
            }
        )
        self.assertTrue(form.is_valid())

    def test_create_driver_with_invalid_license(self):
        form = DriverCreationForm(
            data={
                "license_number": "INVALID!!!",
                "username": "another_test_username",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "first_name": "test",
                "last_name": "test",
            }
        )
        self.assertFalse(form.is_valid())

    def test_passwords_do_not_match(self):
        form = DriverCreationForm(
            data={
                "username": "newdriver",
                "password1": "strongpass123",
                "password2": "wrongpass",
                "license_number": "ABC12345",
                "first_name": "Test",
                "last_name": "User",
            }
        )
        self.assertFalse(form.is_valid())


class CarFormTests(TestCase):
    def test_can_save_car_with_drivers(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )
        self.car = Car.objects.create(model="TestModel",
                                      manufacturer=self.manufacturer)
        self.driver = get_user_model().objects.create_user(
            license_number="LIC12345",
            username="testuser",
            password="StrongPass123!",
            first_name="Test",
            last_name="User",
        )
        form_data = {
            "model": "CarTestModel",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save(commit=False)
        car.save()
        form.save_m2m()
        self.assertIn(self.driver, car.drivers.all())


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="user_" + get_random_string(6),
            password="StrongPass123!",
            first_name="Test",
            last_name="User",
            license_number="LIC" + get_random_string(6),
        )

    def test_valid_license_update(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver, data={"license_number": "XYZ54522"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_license_update(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver, data={"license_number": "BAD!!"}
        )
        self.assertFalse(form.is_valid())
