from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford Edge",
            country="USA"
        )
        self.assertEqual(str(manufacturer), "Ford Edge USA")

    def test_driver_str(self):
        user = get_user_model().objects.create(
            username="exargo",
            password="<PASSWORD>",
            email="<EMAIL>",
            first_name="vadym",
            last_name="vyshnevskyi",
        )
        self.assertEqual(str(user), "exargo (vadym vyshnevskyi)")

    def test_driver_creation(self):
        username = "exargo"
        password = "79zilivi"
        license_number = "ABD12345"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(user.license_number, license_number)
        self.assertEqual(user.check_password(password), True)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        car = Car.objects.create(
            model="Mazda CX-5",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "Mazda CX-5")
