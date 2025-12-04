from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer

from taxi.forms import (
    CarForm,
    DriverLicenseUpdateForm,
)


class CarFormTests(TestCase):
    def test_valid_car_creation(self):
        form = CarForm(
            {
                "model": "Model S",
                "manufacturer": Manufacturer.objects.create(
                    name="Tesla", country="USA"
                ),
                "drivers": [
                    Driver.objects.create(
                        license_number="ABC12345",
                    )
                ],
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_car_creation(self):
        form = CarForm(
            {
                "model": "",
                "manufacturer": "",
                "drivers": [],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)
        self.assertIn("manufacturer", form.errors)
        self.assertIn("drivers", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    @staticmethod
    def update_driver(license_number):
        return DriverLicenseUpdateForm(
            data={
                "license_number": license_number,
            }
        )

    def test_valid_license_number(self):
        self.assertTrue(self.update_driver("ABC12345").is_valid())

    def test_invalid_license_number_length(self):
        self.assertFalse(self.update_driver("AB12345").is_valid())
        self.assertFalse(self.update_driver("ABC123456").is_valid())
        self.assertFalse(self.update_driver("ABCD123456").is_valid())
        self.assertFalse(self.update_driver("AB123456").is_valid())
        self.assertFalse(self.update_driver("abc12345").is_valid())
