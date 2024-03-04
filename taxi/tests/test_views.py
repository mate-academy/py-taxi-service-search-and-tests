from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicViewTest(TestCase):
    def test_login_required(self):
        urls = [
            CAR_LIST_URL,
            DRIVER_LIST_URL,
            MANUFACTURER_LIST_URL,
        ]
        for url in urls:
            self.assertNotEqual(
                self.client.get(url).status_code, 200
            )


class PrivateViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        self.test_password = "Test1234"
        self.user = get_user_model().objects.create_user(
            username="admin.test",
            license_number="ABC12345",
            first_name="Test_first_name",
            last_name="Test_last_name",
            password=self.test_password
        )
        self.client.force_login(self.user)

    def test_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
