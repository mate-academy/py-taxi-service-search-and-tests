from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivetManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test Username",
            first_name="test first",
            last_name="test last",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="Test Country2"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))

        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")

    def test_search_driver_by_username(self) -> None:
        Driver.objects.create(username="ahmed", license_number="TST12345")

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ahmed"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm
        )
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="ahmed"),
        )

    def test_search_car_by_model(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )
        Car.objects.create(model="AMG", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "AMG"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="AMG"),
        )

    def test_search_manufacturer_by_name(self) -> None:
        Manufacturer.objects.create(name="Mercedes", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Mercedes"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="Mercedes"),
        )
