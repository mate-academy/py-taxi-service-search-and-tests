from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicTaxiTests(TestCase):
    def test_login_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_create(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Ford")

        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1",
            password="driverpass1",
            license_number="AB1234561"
        )
        Driver.objects.create(
            username="driver2",
            password="driverpass2",
            license_number="AB1234562"
        )

        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
