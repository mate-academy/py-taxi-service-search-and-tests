from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.create_user(
            license_number="QWS22113",
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str_and_license_number(self):
        driver = get_user_model().objects.get(username="test_username")

        self.assertEqual(str(driver), f"test_username (test_first_name test_last_name)")
        self.assertTrue(driver.license_number)

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.get(username="test_username")
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        driver = get_user_model().objects.get(username="test_username")
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        car.drivers.add(driver)

        self.assertEqual(str(car), car.model)
