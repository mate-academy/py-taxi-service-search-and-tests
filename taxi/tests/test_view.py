from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
INDEX_URL = reverse("taxi:index")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTests(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test", country="test")
        Manufacturer.objects.create(name="test1", country="test1")
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="username", password="password", license_number="AAA12345"
        )
        get_user_model().objects.create_user(
            username="username1",
            password="password1",
            license_number="AAA54321",
        )
        res = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(model="test", manufacturer=manufacturer)
        Car.objects.create(model="test1", manufacturer=manufacturer)
        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")
