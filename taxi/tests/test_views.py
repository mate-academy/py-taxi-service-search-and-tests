from urllib import response

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from setuptools.command.egg_info import manifest_maker

from taxi.models import Manufacturer, Car

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="testAAA11111",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="john_smith",
            password="password123",
            license_number="BBB22222",
        )

        get_user_model().objects.create_user(
            username="anna_lee",
            password="password123",
            license_number="CCC33333",
        )

    def test_retrieve_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["driver_list"])[:5],
            list(drivers)[:5],
        )

    def test_search_driver_by_username(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "john"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "john_smith")
        self.assertNotContains(res, "anna_lee")

    def test_search_driver_by_username_no_match(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "nonexistent"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "john_smith")
        self.assertNotContains(res, "anna_lee")

    def test_search_driver_empty_query_returns_all(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "john_smith")
        self.assertContains(res, "anna_lee")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

    def test_retrieve_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.select_related("manufacturer")
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars),
        )

    def test_search_car_by_model(self):
        res = self.client.get(CAR_LIST_URL, {"model": "Camry"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Camry")
        self.assertNotContains(res, "Corolla")

    def test_search_car_partial_match(self):
        res = self.client.get(CAR_LIST_URL, {"model": "cor"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Camry")
        self.assertContains(res, "Corolla")

    def test_search_car_no_match(self):
        res = self.client.get(CAR_LIST_URL, {"model": "Golf"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Camry")
        self.assertNotContains(res, "Corolla")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Mercedes", country="Germany")

    def test_retrieve_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )

    def test_search_manufacturer_by_name(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Mercedes")

    def test_search_manufacturer_no_match(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "nonexistent"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Toyota")
        self.assertNotContains(res, "Mercedes")
