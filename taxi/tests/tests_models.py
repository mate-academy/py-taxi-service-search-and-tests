from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_model_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_car_model_str(self):
        manufacturer = Manufacturer.objects.create(name="Alpha Romeo",
                                                   country="Italy")
        car = Car.objects.create(model="Julia", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_model_str(self):
        driver = get_user_model().objects.create(
            username="Dimitrios",
            password="<PASSWORD>",
            first_name="Dmitriy",
            last_name="Dobkin"
        )
        self.assertEqual(str(driver), f"{driver.username}"
                                      f" ({driver.first_name}"
                                      f" {driver.last_name})")

    def test_create_driver_with_license(self):
        username = "Dimitrios"
        password = "<PASSWORD>"
        license_number = "AB12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
