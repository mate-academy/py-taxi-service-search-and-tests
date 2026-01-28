from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_string(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test contry"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_string(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            first_name="test first name",
            last_name="test last name",
            password="test password"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url_is_true(self):
        driver = get_user_model().objects.create_user(
            username="test username",
            first_name="test first name",
            last_name="test last name",
            password="test password"
        )
        url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(
            driver.get_absolute_url(),
            url
        )

    def test_car_string(self):
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer1",
            country="test country1"
        )
        driver = get_user_model().objects.create_user(
            username="test username4",
            password="test password"
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)

        self.assertEqual(str(car), car.model)
