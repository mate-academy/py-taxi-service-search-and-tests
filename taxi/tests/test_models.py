from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )
        self.driver = get_user_model().objects.create_user(
            username="test111",
            password="paSS1ord",
            license_number="ABC76594",
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="CBR-1000",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

        self.assertEqual(str(car), car.model)


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} - {manufacturer.country}"
        )


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test111",
            password="paSS1ord",
            license_number="ABC76594",
            first_name="John",
            last_name="Doe"
        )

    def test_driver_str(self):
        expected_str = (f"{self.driver.username} "
                        f"({self.driver.first_name} "
                        f"{self.driver.last_name})")
        self.assertEqual(str(self.driver), expected_str)

    def test_driver_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertEqual(url, f"/drivers/{self.driver.pk}/")
