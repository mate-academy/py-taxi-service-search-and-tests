from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTaxiTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="test123",)
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="test123",
            first_name="Test First",
            last_name="Test Last",
            license_number="JOD26458",)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Company",
            country="Test Country",)

        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,)
        self.car.drivers.add(self.driver)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers))

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars))

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers))

    def test_create_user(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "JOG26458",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
