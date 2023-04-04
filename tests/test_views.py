from django.urls import reverse
from django.contrib.auth import get_user_model

from django.test import TestCase, Client

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")

URL_LIST = [MANUFACTURER_URL, CAR_URL, DRIVER_URL]


class PublicViewsListsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        for url in URL_LIST:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test12345",

        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test1"
        )

        self.user = get_user_model().objects.create_user(
            username="test1",
            password="somestupidpass2345",
            first_name="Test first",
            last_name="Test last",
            license_number="ABC12345"

        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(model="test1", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
