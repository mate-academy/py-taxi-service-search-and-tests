from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_string(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazeratti",
            country="Italy"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_string(self):
        driver = get_user_model().objects.create_user(
            username="anton_best",
            password="anton12345",
            first_name="Anton",
            last_name="Best",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_string(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazeratti",
            country="Italy"
        )
        car = Car.objects.create(
            model="ART1234",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        username = "anton"
        password = "12345anton"
        license_number = "AA1001AO"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_get_absolute_url(self):
        self.driver = get_user_model().objects.create_user(
            username="anton_best",
            password="anton12345",
            first_name="Anton",
            last_name="Best",
            license_number="AA01234AO",
        )
        driver_url = self.driver.get_absolute_url()
        url_expected = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk},
        )

        self.assertEqual(url_expected, driver_url)
