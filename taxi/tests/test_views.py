from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicDriverTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username.test",
            password="password132"
        )
        self.client.force_login(self.user)

    def test_login_required(self):
        Driver.objects.create(
            username="TEst username",
            password="testpassword123",
            license_number="12345678"
        )

        response = self.client.get(DRIVER_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicCarTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username.test",
            password="password132"
        )
        self.client.force_login(self.user)

    def test_login_required(self):
        Car.objects.create(
            model="Test model",
            manufacturer=Manufacturer.objects.create(
                name="test name",
                country="test country"
            )
        )
        response = self.client.get(CAR_URL)

        drivers = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicManufacturerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username.test",
            password="password132"
        )
        self.client.force_login(self.user)

    def test_login_required(self):
        Manufacturer.objects.create(
            name="test name",
            country="Ukraine"
        )
        response = self.client.get(MANUFACTURER_URL)

        drivers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
