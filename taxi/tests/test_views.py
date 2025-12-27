from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Testname",
            country="Testcountry",
        )
        Manufacturer.objects.create(
            name="Name",
            country="Country",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        form_data = {
            "username": "nameuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "LLL12345",
            "first_name": "First",
            "last_name": "Last",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, "First")
        self.assertEqual(new_user.last_name, "Last")
        self.assertEqual(new_user.license_number, "LLL12345")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Testname",
            country="Testcountry",
        )
        get_user_model().objects.create(
            username="nameuser",
            password="testpass123",
            license_number="LLL12345",
        )
        get_user_model().objects.create(
            username="nameuser2",
            password="testpass1234",
            license_number="LLW12345",
        )
        car = Car.objects.create(
            model="Testmodel",
            manufacturer=manufacturer,
        )
        drivers = get_user_model().objects.all()
        car.drivers.set(drivers)
        self.assertEqual(car.model, "Testmodel")
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertEqual(list(car.drivers.all()), list(drivers))
