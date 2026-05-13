from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.driver = user_model.objects.create_user(
            username="test",
            password="test",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )

    def test_driver_str(self):
        expected_result = (
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_result)

    def test_driver_absolute_url(self):
        self.assertEqual(
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver.pk}
            ),
            self.driver.get_absolute_url()
        )


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
