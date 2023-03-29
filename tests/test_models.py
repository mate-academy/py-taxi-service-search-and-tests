from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


PASSWORD = "test_password"
USERNAME = "test_username"
LICENSE_NUMBER = "test_license_number"


class TestsModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="test_name", country="test_country")

        get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
            first_name="test_first_name",
            last_name="test_last_name",
            license_number=LICENSE_NUMBER,
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        manufacturer = Manufacturer.objects.get(id=1)
        ordering = manufacturer._meta.ordering

        self.assertEquals(ordering[0], "name")

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license(self):
        driver = get_user_model().objects.last()

        self.assertEqual(driver.username, USERNAME)
        self.assertTrue(driver.check_password(PASSWORD))
        self.assertEqual(driver.license_number, LICENSE_NUMBER)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
