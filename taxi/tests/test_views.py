from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicTest(TestCase):   # not REGISTERED users
    def test_home_login_required(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.url, "/accounts/login/?next=/")

    def test_drivers_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.url, "/accounts/login/?next=/drivers/")

    def test_cars_login_required(self):
        res = self.client.get(CARS_URL)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.url, "/accounts/login/?next=/cars/")

    def test_manufacturers_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)
        self.assertEqual(res.url, "/accounts/login/?next=/manufacturers/")


class PrivateTest(TestCase):  # REGISTERED users
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(name="testname1")
        self.manufacturer2 = Manufacturer.objects.create(name="testname2")
        self.car1 = Car.objects.create(
            model="testname1",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="testname2",
            manufacturer=self.manufacturer2
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="driver1",
            password="password111",
            license_number="AAA12345",
            first_name="One",
            last_name="FirstDriver",
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="password222",
            license_number="BBB12345",
            first_name="Two",
        )
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
