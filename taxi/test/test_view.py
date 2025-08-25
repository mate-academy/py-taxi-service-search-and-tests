from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_format(self):
        Manufacturer.objects.create(name="test", country="Test")
        Manufacturer.objects.create(name="test2", country="Test2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="TEST", country="Test")
        Manufacturer.objects.create(name="Test", country="Test")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "TEST"})
        self.assertContains(response, "TEST")
        self.assertContains(response, "Test")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)
        Driver.objects.create_user(
            username="test1", password="test123", license_number="ASD12345")
        Driver.objects.create_user(
            username="test2", password="test123", license_number="ASD54321")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test1"})
        self.assertContains(response, "test1")
        self.assertNotContains(response, "test2")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user", password="test123"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(name="TEST", country="Test")
        Car.objects.create(model="A1", manufacturer=manufacturer)
        Car.objects.create(model="A2", manufacturer=manufacturer)

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "A1"})
        self.assertContains(response, "A1")
        self.assertNotContains(response, "A2")
