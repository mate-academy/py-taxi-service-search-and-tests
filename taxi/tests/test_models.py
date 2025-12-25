from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="test")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(username="test",
                                                 first_name="test",
                                                 last_name="test")
        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        car = Car.objects.create(model="test",
                                 manufacturer=Manufacturer.objects.create(
                                     name="test",
                                     country="test"
                                 ))
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        first_name = "test"
        last_name = "test"
        license_number = "TST12345"
        password = "<PASSWORD>"

        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            password=password)

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_get_absolute_url_in_driver(self):
        driver = get_user_model().objects.create_user(username="test",
                                                      first_name="test",
                                                      last_name="test")
        self.assertEqual(driver.get_absolute_url(),
                         reverse("taxi:driver-detail",
                                 kwargs={"pk": driver.pk}))
