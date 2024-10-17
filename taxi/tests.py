from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="tester",
            last_name="test",
            license_number="AMD12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="r6",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
