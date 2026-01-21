from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.manufacturer_one = Manufacturer.objects.create(
            country="test_country_one",
            name="test_manufacturer_one",
        )
        self.manufacturer_two = Manufacturer.objects.create(
            country="test_country_two",
            name="test_manufacturer_two",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        literary_formats = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(literary_formats),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "test_manufacturer_one"}
        )
        self.assertContains(response, self.manufacturer_one.name)
        self.assertNotContains(response, self.manufacturer_two.name)


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@test.com",
            password="password",
            license_number="ASD12345",
        )
        manufacturer = Manufacturer.objects.create(
            country="test_country",
            name="test_manufacturer",
        )
        self.first_car = Car.objects.create(
            manufacturer=manufacturer,
            model="test_model_one",
        )
        self.second_car = Car.objects.create(
            manufacturer=manufacturer,
            model="test_model_two",
        )
        self.first_car.drivers.set([self.user])
        self.second_car.drivers.set([self.user])
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_cars(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "test_model_one"}
        )
        self.assertContains(response, self.first_car.model)
        self.assertNotContains(response, self.second_car.model)


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user_one = get_user_model().objects.create_user(
            username="test_user_1",
            email="test@test.com",
            password="password",
            license_number="ASD12345",
        )
        self.user_two = get_user_model().objects.create_user(
            username="test_user_2",
            email="test@test_2.com",
            password="password",
            license_number="ASD33333",
        )
        self.manufacturer = Manufacturer.objects.create(
            country="test_country",
            name="test_manufacturer",
        )
        self.first_car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="test_model_one",
        )
        self.second_car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="test_model_two",
        )
        self.first_car.drivers.set([self.user_one, self.user_two])
        self.second_car.drivers.set([self.user_one])
        self.client.force_login(self.user_one)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test_user_1"}
        )
        self.assertContains(response, self.user_one.username)
        self.assertNotContains(response, self.user_two.username)
