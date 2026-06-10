from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTest(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="testcountry"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="testcountry"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test1",
            first_name="testcountry",
            last_name="test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license(self):
        username = "test1"
        password = "123teste"
        license_number = "TES12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_get_absolute_url(self):
        username = "test1"
        password = "123teste"
        license_number = "TES12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )
