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
        self.user = Driver.objects.create_user(
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

    def test_car_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_driver_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)


class ManufacturerListViewTest(TestCase):
    def test_search_form_in_context(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerSearchForm
        )

        response = self.client.get(CAR_LIST_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            CarSearchForm
        )

        response = self.client.get(DRIVER_LIST_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )
