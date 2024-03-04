from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacture_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="strong_test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(drivers),
            list(response.context["driver_list"])
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Banderomobile",
            country="Ukrainian_Empire"
        )
        Car.objects.create(
            model="Test_model",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Test_model2",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        all_car = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(all_car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacture(self):
        Manufacturer.objects.create(
            name="Test",
            country="TEST_Empire"
        )
        Manufacturer.objects.create(
            name="Banderomobile",
            country="Ukrainian_Empire"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
