from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ManufacturerModelTests(TestCase):
    name_manufacturer = "test"
    country_manufacturer = "Germany"

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name=self.name_manufacturer, country=self.country_manufacturer
        )
        self.assertEqual(
            str(manufacturer),
            f"{self.name_manufacturer} {self.country_manufacturer}"
        )

    def test_ordering_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Tesla", country="USA")

        manufacturers = Manufacturer.objects.all()
        names = [manufacturer.name for manufacturer in manufacturers]

        self.assertEqual(names, ["Audi", "BMW", "Tesla"])


class CarModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="USA"
        )
        car = Car.objects.create(model="TestCar", manufacturer=manufacturer)

        self.assertEqual(str(car), "TestCar")


class DriverModelTests(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="driver1",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.assertEqual(str(driver), "driver1 (John Doe)")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="driver2",
            password="test12345",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ98765",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
