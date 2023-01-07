from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTestForm(TestCase):
    def test_logic_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "user.test",
            "passwordtest123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Mazda")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "user.test",
            "passwordtest123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW")
        manufacturer2 = Manufacturer.objects.create(name="Mazda")
        Car.objects.create(model="M3", manufacturer=manufacturer1)
        Car.objects.create(model="CX-90", manufacturer=manufacturer2)

        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTestForm(TestCase):
    def test_logic_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "user.test",
            "passwordtest123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(license_number="Test license")

        response = self.client.get(DRIVER_URL)
        driver = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
