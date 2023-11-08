from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver
from .get_user_model_function import get_user_model_function

MANU_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANU_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="name",
            country="country",
        )
        res = self.client.get(MANU_URL)
        self.assertEqual(res.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        driver = get_user_model_function()
        car = Car.objects.create(
            model="test_car",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])

        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(res, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self) -> None:
        get_user_model_function()

        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )

        self.assertTemplateUsed(res, "taxi/driver_list.html")
