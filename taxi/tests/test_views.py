from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePagesAndSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123vc123a"
        )
        self.client.force_login(self.user)

    def test_retrieve_and_search(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Test11",
            country="USA"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Test22",
            country="USB"
        )
        Car.objects.create(model="model_A", manufacturer=manufacturer_1)
        Car.objects.create(model="model_B", manufacturer=manufacturer_2)

        # Manufacturer Test

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        response = self.client.get(MANUFACTURER_URL, {"name": "Test11"})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["manufacturer_list"])
        self.assertEqual(len(result), 1)

        response = self.client.get(MANUFACTURER_URL, {"name": ""})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["manufacturer_list"])
        self.assertEqual(len(result), 2)

        # Car Test

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

        response = self.client.get(CAR_URL, {"model": "model_A"})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["car_list"])
        self.assertEqual(len(result), 1)

        response = self.client.get(CAR_URL, {"model": ""})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["car_list"])
        self.assertEqual(len(result), 2)

        # Driver Test

        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

        response = self.client.get(DRIVER_URL, {"username": "test"})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["driver_list"])
        self.assertEqual(len(result), 1)

        response = self.client.get(DRIVER_URL, {"username": "aaaa"})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["driver_list"])
        self.assertEqual(len(result), 0)
