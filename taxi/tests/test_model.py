from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Manufacturer1")
        get_user_model().objects.create_user(username="test_user",
                                             password="test_user_password228",
                                             first_name="Global",
                                             last_name="Test")
        Car.objects.create(model="BMW",
                           manufacturer_id=1)

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        expected_str = (f"{driver.username} "
                        f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), expected_str)

    def test_driver_method_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_str)
