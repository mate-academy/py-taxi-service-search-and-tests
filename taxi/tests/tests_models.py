from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Car, Driver, Manufacturer


class ModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Aa1234554321",
            license_number="ABC01234",
        )
        self.client.force_login(self.admin_user)
        self.driver_one = Driver.objects.create(
            username="driver_one",
            password="Aa1234554321",
            license_number="ABC11111",
        )
        self.manufacturer_one = Manufacturer.objects.create(
            name="Manufacturer_one",
            country="Ukraine",
        )

    def test_car_model(self):
        car = Car.objects.create(
            manufacturer=self.manufacturer_one,
            model="Car_one"
        )
        car.drivers.add(self.driver_one)
        self.assertEqual(str(car), str(car.model))
