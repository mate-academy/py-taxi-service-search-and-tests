from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1223",
            first_name="test_first",
            last_name="test_last",
            license_number="TST12345"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(name="TestName", country="TestCountry")
        Manufacturer.objects.create(name="Bora", country="Baron")
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_form_in_context(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )

    def test_manufacturer_search_filter(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(
            MANUFACTURER_LIST_URL + "?manufacturer=Toyota"
        )
        manufacturers = response.context["manufacturer_list"]

        # Перевір, що тільки Toyota в результатах
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")

        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        # Перевір, що тільки Toyota в результатах
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertEqual(
            list(manufacturers),
            list(response.context["manufacturer_list"]))


class SearchTests(TestCase):
    def setUp(self):
        # Створюємо тестові дані
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="john_doe",
            password="test12345",
            license_number="ABC12345"
        )

        self.client.force_login(self.driver)

    def test_car_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            CarSearchForm
        )

    def test_driver_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )
