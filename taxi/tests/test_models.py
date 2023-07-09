from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test username",
            password="test12345test",
            first_name="first test",
            last_name="last test"
        )
        Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_manufacurer_str(self):
        format_ = Manufacturer.objects.get(id=1)

        self.assertEqual(str(format_), f"{format_.name} {format_.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_driver_model_verbose_and_plural_name(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver._meta.verbose_name, "driver")
        self.assertEqual(driver._meta.verbose_name_plural, "drivers")

    def test_car_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(str(car), car.model)
