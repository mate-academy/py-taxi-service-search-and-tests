from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car
from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)


MANUFACTURER_URL = reverse("taxi:manufacturer-list")

DRIVER_URL = reverse("taxi:driver-list")

CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test", country="USA")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertTrue(response.context["search_form"])

    def test_manufacturer_page_search_form(self):
        data = {
            "first_case": {"name": "test12"},
            "second_case": {"name": "Test34"},
            "third_case": {"name": "test5"},
            "country": "Ukraine"
        }

        Manufacturer.objects.create(
            name=data["first_case"]["name"],
            country=data["country"]
        )
        Manufacturer.objects.create(
            name=data["second_case"]["name"],
            country=data["country"]
        )
        response = self.client.get(MANUFACTURER_URL, data=data["first_case"])
        self.assertContains(response, data["first_case"]["name"])
        self.assertNotContains(response, data["second_case"]["name"])

        response = self.client.get(MANUFACTURER_URL, data=data["third_case"])
        self.assertNotContains(response, data["country"])


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")
        self.assertTrue(res.context["search_form"])

    def test_driver_page_search_form(self):
        data = {
            "first_case": {"username": "test12"},
            "second_case": {"username": "Test34"},
            "password": "test1234",
            "license_number1": "1234test",
            "license_number2": "test1234"
        }

        get_user_model().objects.create_user(
            username=data["first_case"],
            password=data["password"],
            license_number=data["license_number1"]
        )
        get_user_model().objects.create_user(
            username=data["second_case"],
            password=data["password"],
            license_number=data["license_number2"]
        )
        response = self.client.get(DRIVER_URL, data=data["first_case"])
        self.assertContains(response, data["first_case"]["username"])
        self.assertNotContains(response, data["second_case"]["username"])


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="testman",
            country="USA"
        )
        Car.objects.create(model="test", manufacturer=manufacturer)
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
        self.assertTrue(res.context["search_form"])

    def test_driver_page_search_form(self):
        manufacturer = Manufacturer.objects.create(
            name="testman",
            country="USA"
        )
        data = {
            "first_case": {"model": "test12"},
            "second_case": {"model": "Test34"},
            "third_case": {"model": "test5"},
        }

        Car.objects.create(
            model=data["first_case"]["model"],
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model=data["second_case"]["model"],
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_URL, data=data["first_case"])
        self.assertContains(response, data["first_case"]["model"])
        self.assertNotContains(response, data["second_case"]["model"])

        response = self.client.get(CAR_URL, data=data["third_case"])
        self.assertNotContains(response, manufacturer.name)
