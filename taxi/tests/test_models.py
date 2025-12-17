from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="zaz",
            country="Ukraine"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="zaz",
            country="Ukraine"
        )
        car = Car.objects.create(model="BMW X3", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "test12"
        cls.password = "testtest"
        cls.license_number = "A1V2B2"
        cls.first_name = "Bob"
        cls.last_name = "Bobovich"

        cls.driver = get_user_model().objects.create_user(
            username=cls.username,
            password=cls.password,
            license_number=cls.license_number,
            first_name=cls.first_name,
            last_name=cls.last_name
        )

    def test_driver_creation_and_fields(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertTrue(self.driver.check_password(self.password))

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_driver_absolute_url(self):
        url = self.driver.get_absolute_url()
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )

        self.assertEqual(url, expected_url)
