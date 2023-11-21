from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1",
            password="driver1pass",
            license_number="QWE12345"
        )
        Driver.objects.create(
            username="driver2",
            password="driver2pass",
            license_number="QWE54321"
        )
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        Car.objects.create(
            model="Grand Cherokee",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Gladiator",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(cars))


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        Manufacturer.objects.create(
            name="Dodge",
            country="USA"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
