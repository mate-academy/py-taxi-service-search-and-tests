from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicListTest(TestCase):
    def test_car_login_required(self):
        result = self.client.get(CAR_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_driver_login_required(self):
        result = self.client.get(DRIVER_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_manufacturer_login_required(self):
        result = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(result.status_code, 200)


class PrivateListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test0451"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="testa",
            country="test"
        )
        Car.objects.create(model="model_test", manufacturer=manufacturer)
        Car.objects.create(model="testreza", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Testa", country="test")
        Manufacturer.objects.create(name="Testa2", country="test2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
