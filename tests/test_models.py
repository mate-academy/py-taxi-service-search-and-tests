from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        name_ = Manufacturer.objects.create(name="test")
        self.assertEqual(str(name_), f"{name_.name} {name_.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test111",
            first_name="Test first",
            last_name="Test last"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test111"
            )
        expected_url = f"/drivers/{driver.pk}/"
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test1", country="Test")
        car = Car.objects.create(model="testA", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
