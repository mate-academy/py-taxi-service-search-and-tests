from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelsTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="testing",
            license_number="ABC12314",
            first_name="user123",
            last_name="test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln Continental",
            country="Germany",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Bentley Continental",
            country="Brazil",
        )

        driver1 = get_user_model().objects.create(
            username="wist",
            license_number="ABC12674",
            first_name="Anatoliy",
            last_name="Repov",
        )

        car = Car.objects.create(
            model="Toyota",
            manufacturer=manufacturer1,
        )

        car.drivers.add(driver1)

        self.assertEqual(
            str(car),
            f"{car.model}"
        )
