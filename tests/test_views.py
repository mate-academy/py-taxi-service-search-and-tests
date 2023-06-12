import pprint

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:driver-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def test_manufacture_list_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturer(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password111")
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Test name", country="Test country")
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password111")
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test",
            "last_name": "Test",
            "license_number": "AAA11111"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PrivateCar(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password111")
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
