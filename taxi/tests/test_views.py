from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URl = reverse("taxi:car-list")
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
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="testname",
            country="Test"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="test"
        )
        searched_name = "test"
        response = self.client.get(MANUFACTURER_URL, name=searched_name)
        self.assertEqual(response.status_code, 200)
        context = Manufacturer.objects.filter(
            name__icontains=searched_name
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(context)
        )


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URl)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="AAA33333"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="tets")
        Car.objects.create(
            model="testmodel",
            manufacturer=manufacturer,
        )
        res = self.client.get(CAR_URl)
        self.assertEqual(res.status_code, 200)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )
        searched_name = "test"
        res = self.client.get(CAR_URl, {"model": searched_name})
        self.assertEqual(res.status_code, 200)
        context = Car.objects.filter(
            model__icontains=searched_name
        )
        self.assertEqual(
            list(res.context["car_list"]), list(context)
        )


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="AAA33333"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="test1",
        )
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)

    #
    def test_search_driver_by_username(self):
        Driver.objects.create(
            username="test23",
        )
        searched_name = "test"
        res = self.client.get(DRIVER_URL, {"username": searched_name})
        self.assertEqual(res.status_code, 200)
        context = Driver.objects.filter(
            username__icontains=searched_name
        ).order_by("username")
        self.assertEqual(
            list(res.context["driver_list"]), list(context)
        )
