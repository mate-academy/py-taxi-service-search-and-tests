from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(
            username="test", first_name="first", last_name="last"
        )
        manufacturer = Manufacturer.objects.create(
            name="test", country="country"
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )

    def test_representation_of_manufacturer(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_representation_of_driver(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_verbose_name(self):
        driver = get_user_model().objects.get(id=1)
        verbose_name = driver._meta.verbose_name
        self.assertEquals(verbose_name, "driver")

    def test_driver_verbose_name_plural(self):
        driver = get_user_model().objects.get(id=1)
        verbose_name = driver._meta.verbose_name_plural
        self.assertEquals(verbose_name, "drivers")

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_representation_of_car(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
