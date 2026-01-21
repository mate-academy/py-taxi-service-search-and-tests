from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mercedes", country="Germany"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_country(self):
        name = "Mercedes"
        country = "Germany"
        manufacturer = Manufacturer.objects.create(name=name, country=country)
        self.assertEqual(manufacturer.country, country)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mercedes", country="Germany"
        )
        car = Car.objects.create(model="GLA250", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Shuma",
            password="test1234",
            first_name="Michael",
            last_name="Shumacher",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url(self):
        username = "Shuma"
        password = "test1234"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_create_driver_with_license_number(self):
        username = "Shuma"
        password = "test1234"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
