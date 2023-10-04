from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testralia"
        )
        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="sasha",
            last_name="test",
            password="12345qwe@",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="sasha",
            last_name="test",
            password="12345qwe@",
        )
        url = f"/drivers/{driver.id}/"
        self.assertEquals(driver.get_absolute_url(), url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testralia"
        )
        car = Car.objects.create(model="testla", manufacturer=manufacturer)
        self.assertEquals(str(car), car.model)
