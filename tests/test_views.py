from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test")
        Manufacturer.objects.create(name="test1")

        res = self.client.get(MANUFACTURER_URL)
        self.assertEquals(res.status_code, 200)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="test")
        searched_name = "test"
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": searched_name}
        )
        self.assertEqual(response.status_code, 200)
        manufacturer_in_context = Manufacturer.objects.filter(
            name__icontains=searched_name
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], manufacturer_in_context
        )


class PublicCarTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
            "IUO45658"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="pass123456",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self):
        Driver.objects.create(username="Test")
        response = self.client.get(DRIVERS_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
