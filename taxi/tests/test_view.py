from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="ASD45231"
        )
        self.manufacturer_opel = Manufacturer.objects.create(
            name="Opel",
            country="Germany",
        )
        self.manufacturer_renault = Manufacturer.objects.create(
            name="Renault",
            country="France",
        )
        self.manufacturer_nissan = Manufacturer.objects.create(
            name="Nissan",
            country="Japan",
        )
        self.car_logan = Car.objects.create(
            model="Logan",
            manufacturer=self.manufacturer_renault,
        )
        self.car_zafira = Car.objects.create(
            model="Zafira",
            manufacturer=self.manufacturer_opel,
        )
        self.car_juke = Car.objects.create(
            model="Juke",
            manufacturer=self.manufacturer_nissan,
        )

    def test_search_by_name_manufacturer(self):
        self.client.force_login(self.user)
        res = self.client.get(MANUFACTURER_URL, {"name": "Nissan"})
        self.assertEqual(res.status_code, 200)
        manufacturer = res.context["manufacturer_list"]
        self.assertIn(self.manufacturer_nissan, manufacturer)
        self.assertNotIn(self.manufacturer_opel, manufacturer)

    def test_search_by_model_car(self):
        self.client.force_login(self.user)
        res = self.client.get(CAR_URL, {"model": "Juke"})
        self.assertEqual(res.status_code, 200)
        cars = res.context["car_list"]
        self.assertIn(self.car_juke, cars)
        self.assertNotIn(self.car_zafira, cars)

    def test_search_form_for_manufacturer_context(self):
        self.client.force_login(self.user)
        response = self.client.get(MANUFACTURER_URL)
        self.assertIn("search_form", response.context)

    def test_search_form_for_car_context(self):
        self.client.force_login(self.user)
        response = self.client.get(CAR_URL)
        self.assertIn("search_form", response.context)


class DriverSearchTest(TestCase):
    def setUp(self):

        self.driver_ivan = get_user_model().objects.create_user(
            username="ivan_petrov", password="AS45", license_number="ASD12312"
        )
        self.driver_oleg = get_user_model().objects.create_user(
            username="oleg_ivanov", password="AS46", license_number="ADB21245"
        )
        self.driver_anna = get_user_model().objects.create_user(
            username="anna_smith", password="AS32", license_number="CAS12345"
        )

    def test_search_by_username_returns_correct_results(self):
        self.client.force_login(self.driver_ivan)
        res = self.client.get(DRIVER_URL, {"username": "ivan"})
        self.assertEqual(res.status_code, 200)
        drivers = res.context["driver_list"]
        self.assertIn(self.driver_ivan, drivers)
        self.assertIn(self.driver_oleg, drivers)

    def test_search_form_is_in_context(self):
        self.client.force_login(self.driver_ivan)
        response = self.client.get(DRIVER_URL)
        self.assertIn("search_form", response.context)
