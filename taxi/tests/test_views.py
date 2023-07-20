from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:

        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123"
        )
        self.client.force_login(self.driver)

    def test_retrieve_car(self):

        response = self.client.get(CAR_URL)
        cars = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password123"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="test_username_1",
            password="test_password_1234",
            license_number="test_license_number1"
        )

        get_user_model().objects.create_user(
            username="test_username_2",
            password="test_password_1234",
            license_number="test_license_number2"
        )
        response = self.client.get(DRIVER_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
