from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test",
            country="Testland"
        )
        Manufacturer.objects.create(
            name="TestCar",
            country="USA"
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        res = self.client.get(MANUFACTURER_URL, {"name": "toy"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "BMW")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="driver1", password="pass123", license_number="AAA11111"
        )
        get_user_model().objects.create_user(
            username="driver2", password="pass456", license_number="BBB22222"
        )

        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")
        self.assertIn("search_form", res.context)

    def test_driver_search_by_username(self):
        get_user_model().objects.create_user(
            username="superdriver", password="123", license_number="CCC33333"
        )
        get_user_model().objects.create_user(
            username="fastguy", password="456", license_number="DDD44444"
        )

        res = self.client.get(DRIVER_URL, {"username": "super"})
        self.assertContains(res, "superdriver")
        self.assertNotContains(res, "fastguy")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_retrieve_cars(self):
        Car.objects.create(model="Model S", manufacturer=self.manufacturer)
        Car.objects.create(model="Model 3", manufacturer=self.manufacturer)

        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
        self.assertIn("search_form", res.context)

    def test_car_search_by_model(self):
        Car.objects.create(model="Mustang", manufacturer=self.manufacturer)
        Car.objects.create(model="Fusion", manufacturer=self.manufacturer)

        res = self.client.get(CAR_URL, {"model": "must"})
        self.assertContains(res, "Mustang")
        self.assertNotContains(res, "Fusion")
