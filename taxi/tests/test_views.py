from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTest(TestCase):
    def test_manufacturers_list_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_cars_list_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_drivers_list_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="mecho",
            password="Secretpw1",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Brichka", country="China")

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="mecho",
            password="Secretpw1",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model X", manufacturer=manufacturer)
        Car.objects.create(model="Cybertruck", manufacturer=manufacturer)

    def test_retrieve_cars_list(self):
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="mecho",
            password="Secretpw1",
        )
        self.client.force_login(self.user)
        Driver.objects.create(
            username="jlock",
            password="Secretpw2",
            license_number="HELLO123"
        )
        Driver.objects.create(
            username="hurley",
            password="Secretpw3",
            license_number="QWE12345"
        )

    def test_retrieve_drivers_list(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")
