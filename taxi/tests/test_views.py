from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class NoLoginAccessTests(TestCase):

    def assert_login_required(self, url):
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_manufacturer_login_required(self):
        self.assert_login_required(MANUFACTURERS_URL)

    def test_car_login_required(self):
        self.assert_login_required(CARS_URL)

    def test_driver_login_required(self):
        self.assert_login_required(DRIVERS_URL)


class ListViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test1", country="TestCountry1")
        Manufacturer.objects.create(name="Test2", country="TestCountry2")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="TestCountry1"
        )
        Car.objects.create(model="Test1", manufacturer=manufacturer)
        Car.objects.create(model="Test2", manufacturer=manufacturer)

        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="Testusername1",
            password="passwd1",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="Testusername2",
            password="passwd2",
            license_number="QWE12345"
        )

        response = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
