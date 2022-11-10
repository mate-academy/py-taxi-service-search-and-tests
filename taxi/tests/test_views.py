from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1213412",
            license_number="AOW20193"
        )
        self.client.force_login(self.user)

    def test_read_manufacturer(self):
        Manufacturer.objects.create(name="Jowa", country="Lopu")
        Manufacturer.objects.create(name="Woks", country="Pored")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1213412",
            license_number="AOW20193"
        )
        self.client.force_login(self.user)

    def test_read_car(self):
        manufacturer = Manufacturer.objects.create(name="Woks", country="Pored")
        Car.objects.create(
            model="Lowes",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Podiw",
            manufacturer=manufacturer,
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))

        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1213412",
            license_number="AOW20193"
        )
        self.client.force_login(self.user)

    def test_read_driver(self):
        Driver.objects.create(
            username="testdata",
            password="newpass927273",
            license_number="OWH28432"
        )
        Driver.objects.create(
            username="t21sada",
            password="adf423ws73",
            license_number="LZJ21235"
        )

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

        self.assertTemplateUsed(response, "taxi/driver_list.html")
