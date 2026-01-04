from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTest(TestCase):
    def test_login_required_manufacturer(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(model="test_model", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(cars),
            list(response.context["car_list"])
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        Driver.objects.create(username="test", license_number="test_license")
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(drivers),
            list(response.context["driver_list"])
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test", country="test")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers),
            list(response.context["manufacturer_list"])
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
