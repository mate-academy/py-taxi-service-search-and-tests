from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from taxi.models import Car, Manufacturer


class DriverCreationFormTests(TestCase):
    def test_valid_data_creates_driver(self):
        form_data = {
            "username": "driver1",
            "password1": "pass12345",
            "password2": "pass12345",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, form_data["username"])
        self.assertEqual(driver.license_number, form_data["license_number"])
        self.assertEqual(driver.first_name, form_data["first_name"])
        self.assertEqual(driver.last_name, form_data["last_name"])

    def test_invalid_license_number(self):
        form_data = {
            "username": "driver2",
            "password1": "pass12345",
            "password2": "pass12345",
            "license_number": "WRONG123",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="pass12345",
            license_number="ABC12345"
        )

    def test_update_valid_license_number(self):
        form_data = {"license_number": "DEF67890"}
        form = DriverLicenseUpdateForm(instance=self.driver, data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.license_number, "DEF67890")

    def test_update_invalid_license_number(self):
        form_data = {"license_number": "BAD"}
        form = DriverLicenseUpdateForm(instance=self.driver, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="pass123",
            license_number="AAA11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="pass123",
            license_number="BBB22222"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_car_form_valid_data(self):
        form_data = {
            "model": "X5",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }

        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())

        car = form.save()

        self.assertEqual(car.model, "X5")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertEqual(
            list(car.drivers.all()),
            [self.driver1, self.driver2]
        )
