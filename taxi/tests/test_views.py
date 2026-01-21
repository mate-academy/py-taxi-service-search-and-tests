from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from functools import wraps

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


def user_setup(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="TST12345"
        )
        self.client.force_login(self.user)
        return func(self, *args, **kwargs)
    return wrapper


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    @user_setup
    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="TOYODA")
        Manufacturer.objects.create(name="General Motors")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    @user_setup
    def test_search_manufacturer(self):
        res = self.client.get(
            MANUFACTURER_URL, data={"name": "test"}
        )
        self.assertContains(res, "test")
        self.assertNotContains(res, "Test2")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    @user_setup
    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    @user_setup
    def test_search_driver(self):
        res = self.client.get(
            DRIVER_URL, data={"username": "test"}
        )
        self.assertContains(res, "test")
        self.assertNotContains(res, "Test2")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    @user_setup
    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(model="test1", manufacturer=manufacturer)
        Car.objects.create(model="test2", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    @user_setup
    def test_search_car(self):
        res = self.client.get(
            CAR_URL, data={"model": "test"}
        )
        self.assertContains(res, "test")
        self.assertNotContains(res, "Test2")
