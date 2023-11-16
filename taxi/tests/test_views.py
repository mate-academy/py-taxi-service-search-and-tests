from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_private",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Wood")
        Manufacturer.objects.create(name="Daewoo")

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers),
                         )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_driver_is_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):

    def test_retrieve_driver(self):
        Driver.objects.create(username="luca_deluca", password="Test123456", license_number="ERU45678")
        Driver.objects.create(username="saverio_deluca", password="Test567890", license_number="ERD45668")
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="Test234534534",
        )
        self.client.force_login(self.user)
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers), )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicCarTest(TestCase):
    def test_car_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def test_retrieve_car(self):
        man1 = Manufacturer.objects.create(name="Wood")
        man2 = Manufacturer.objects.create(name="Daewoo")
        Car.objects.create(model="trent", manufacturer=man1)
        Car.objects.create(model="Camry", manufacturer=man2)
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="Test234534534",
        )
        self.client.force_login(self.user)
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

