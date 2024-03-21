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

    def test_login_required(self):
        response_drv = self.client.get(DRIVER_URL)
        response_car = self.client.get(CAR_URL)
        response_manufacturer = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response_drv.status_code, 200)
        self.assertNotEqual(response_car.status_code, 200)
        self.assertNotEqual(response_manufacturer.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test_pass"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(drivers),
            list(response.context["driver_list"])
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_car(self):
        Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
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
            name="Tesla",
            country="USA"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_toggle_assign_to_car(self):
        self.client.login(username="testadmin", password="test123123")
        car = Car.objects.create(model="Camry",
                                 manufacturer=self.manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
