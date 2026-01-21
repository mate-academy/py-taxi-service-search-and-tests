from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create(
            username="testuser",
            first_name="John",
            last_name="Doe"
            # Add any other required fields here for your Driver model
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])

    def test_manufacturer_str(self):
        self.assertEquals(str(
            self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self):
        self.assertEquals(str(self.car), self.car.model)

    def test_driver_str(self):
        self.assertEquals(str(
            self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )

    def test_create_driver_with_license(self):
        username = "testusers"
        password = "1235446df"
        license_number = "AMD12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
