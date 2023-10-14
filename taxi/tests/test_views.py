from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEquals(response.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEquals(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="lewis.hamilton",
            password="12password34",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Seat", country="Spain")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_field_manufacturer(self):
        searched_name = "Seat"
        response = self.client.get(MANUFACTURERS_URL, {"name": searched_name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["manufacturer_list"][0],
            Manufacturer.objects.get(name=searched_name)
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="lewis.hamilton",
            password="12password34",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="testuser1",
            password="123password45",
            license_number="BCD23456"
        )
        get_user_model().objects.create_user(
            username="testuser2",
            password="12password345",
            license_number="CDE34567"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_search_field_driver(self):
        searched_username = "testuser1"
        response = self.client.get(
            DRIVERS_URL, {"username": searched_username}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["driver_list"][0],
            Driver.objects.get(username=searched_username)
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="lewis.hamilton",
            password="12password34",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Mustang", manufacturer=manufacturer)
        Car.objects.create(model="Mondeo", manufacturer=manufacturer)

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_search_field_car(self):
        searched_model = "Mustang"
        response = self.client.get(CARS_URL, {"model": searched_model})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["car_list"][0],
            Car.objects.get(model=searched_model)
        )
