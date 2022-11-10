from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Lol kek 221",
            country="Super great country"
        )
        self.assertEqual(
            str(manufacturer),
            "Lol kek 221 Super great country"
        )

    def test_driver_is_user_class(self):
        self.assertIs(Driver, get_user_model())

    def test_driver_str_without_full_name(self):
        driver = Driver.objects.create_user(
            username="usercheck",
            password="checker123",
            email="check@chacha.com",
        )
        self.assertEqual(
            str(driver),
            "usercheck"
        )

    def test_driver_str_with_full_name(self):
        driver = Driver.objects.create_user(
            username="usercheck2",
            password="checker1232",
            email="check2@chacha.com",
            first_name="Lol",
            last_name="Kek",
        )
        self.assertEqual(
            str(driver),
            "usercheck2 (Lol Kek)"
        )

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="newuser123",
            password="checker123",
            email="newuser@chacha.com",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.id})
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Lol kek 321",
            country="Super great country"
        )

        car = Car.objects.create(
            model="Supercar",
            manufacturer=manufacturer
        )

        self.assertEqual(
            str(car),
            "Supercar"
        )
