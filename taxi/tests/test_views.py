from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="teat1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Ferrari", country="Italy")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class SearchTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Alice",
            license_number="ABC12345",
            password="test-password",
        )
        self.client.force_login(self.driver)

    def test_search_drivers_by_username(self):
        get_user_model().objects.create_user(
            username="Bob",
            license_number="DEF67890",
            password="test-password",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "ali"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), [self.driver])

    def test_search_cars_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        expected_car = Car.objects.create(
            model="Corolla", manufacturer=manufacturer
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cor"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), [expected_car])

    def test_search_manufacturers_by_name(self):
        expected_manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [expected_manufacturer],
        )
