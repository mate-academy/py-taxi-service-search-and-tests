from http import client

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car
from taxi.views import CarListView

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testname",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Tesla")
        Manufacturer.objects.create(country="USA")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testname",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(
            model="Tesla",
            manufacturer=Manufacturer.objects.create(
                name="Tesla",
                country="USA"
            ),
            id=1
        )
        Car.objects.create(
            model="Nissan",
            manufacturer=Manufacturer.objects.create(
                name="Nissan",
                country="Japan"
            ),
            id=2
        )
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_get_context_data_contains_search_form(self):
        response = self.client.get(CAR_LIST_URL, {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        search_form = response.context["search_form"]
        self.assertIsInstance(search_form, CarSearchForm)
        self.assertEqual(search_form.initial["model"], "")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testname",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        format_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "HFJ12341",
        }
        self.client.post(reverse("taxi:driver-create"), data=format_data)
        new_user = get_user_model().objects.get(
            username=format_data["username"]
        )

        self.assertEqual(new_user.first_name, format_data["first_name"])
        self.assertEqual(new_user.last_name, format_data["last_name"])
        self.assertEqual(
            new_user.license_number, format_data["license_number"]
        )
