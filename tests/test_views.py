from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTests(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="Fiesta", manufacturer=ford)
        Car.objects.create(model="X5", manufacturer=bmw)

        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser2",
            password="password123",
            license_number="ABC00000"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1",
            password="password123",
            license_number="ABC12395",
        )
        Driver.objects.create(
            username="driver2",
            password="password123",
            license_number="ABC12396",
        )
        res = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser3",
            password="password123",
            license_number="ABC00000"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
