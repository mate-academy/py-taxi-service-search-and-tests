from http import client

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")
CAR_FORMAT_URL = reverse("taxi:car-list")
DRIVER_FORMAT_URL = reverse("taxi:driver-list")


class PublicManufacturerFormatTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test", country="Test")
        Manufacturer.objects.create(name="test2", country="Test2")
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCarFormatTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Test"
        )
        Car.objects.create(manufacturer=manufacturer, model="Test")
        Car.objects.create(manufacturer=manufacturer, model="Test2")
        res = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))


class PublicDriverFormatTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)
        Driver.objects.create(
            username="driver1",
            license_number="TES12345"
        )
        Driver.objects.create(
            username="driver2",
            license_number="TES22345"
        )

    def test_retrieve_driver(self):

        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")
