from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class TestSearchForms(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Lincoln",
            country="USA"
        )

        self.driver_1 = Driver.objects.create(
            license_number="AAA11111",
            username="joyce",
            first_name="Joyce",
            last_name="Byers"
        )
        self.driver_2 = Driver.objects.create(
            license_number="BBB22222",
            username="hopper",
            first_name="Jim",
            last_name="Hopper"
        )

        self.car_1 = Car.objects.create(
            model="X5 M",
            manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="Lincoln Continental",
            manufacturer=self.manufacturer_2
        )

        self.car_1.drivers.add(self.driver_1)
        self.car_2.drivers.add(self.driver_2)

    def test_drivers_username_search(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url, {"username": "joyce"})

        self.assertContains(res, self.driver_1.username)
        self.assertNotContains(res, self.driver_2.username)

    def test_cars_model_search(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url, {"model": "X5 M"})

        self.assertContains(res, self.car_1.model)
        self.assertNotContains(res, self.car_2.model)

    def test_manufacturers_name_search(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url, {"name": "BMW"})

        self.assertContains(res, self.manufacturer_1.name)
        self.assertNotContains(res, self.manufacturer_2.name)
