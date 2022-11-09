from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "testdriver",
            "user12345")
        self.client.force_login(self.user)

    def test_driver_create(self):
        form_data = {
            "username": "testuser",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "firsttest",
            "last_name": "lasttest",
            "license_number": "AAA12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        test_user = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(test_user.first_name, form_data["first_name"])
        self.assertEqual(test_user.last_name, form_data["last_name"])
        self.assertEqual(test_user.license_number, form_data["license_number"])


class PublicCarsTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="Rav4",
            manufacturer=toyota
        )
        Car.objects.create(
            model="M5",
            manufacturer=bmw
        )

        response = self.client.get(CAR_URL)
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="user12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        Manufacturer.objects.create(
            name="BMW",
            country="Germany")
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
