from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        Car.objects.create(
            model="New model",
            manufacturer=manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "778899oo",
            "password2": "778899oo",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "AAA12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
