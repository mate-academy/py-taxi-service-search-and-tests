from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

HOME_URL = reverse("taxi:index")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicTests(TestCase):
    def test_login_required(self):
        res_home = self.client.get(HOME_URL)
        res_drivers = self.client.get(DRIVERS_URL)
        res_cars = self.client.get(CARS_URL)
        res_manufacturers = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res_home.status_code, 200)
        self.assertNotEqual(res_drivers.status_code, 200)
        self.assertNotEqual(res_cars.status_code, 200)
        self.assertNotEqual(res_manufacturers.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1345"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVERS_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
