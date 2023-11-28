from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


car_url = reverse("taxi:car-list")
driver_url = reverse("taxi:driver-list")
manufacturer_url = reverse("taxi:manufacturer-list")


class PublicCartTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(car_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="QWE12345h"
        )
        self.client.force_login(self.user)

    def test_receive_car(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Accord", manufacturer=manufacturer1)
        Car.objects.create(model="Thundra", manufacturer=manufacturer1)

        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(driver_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_receive_drivers(self):
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)

        drivers = list(Driver.objects.all())
        self.assertEqual(
            list(response.context["driver_list"]),
            drivers
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(manufacturer_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_receive_manufacturers(self):
        Manufacturer.objects.create(
            name="testm",
            country="TestM"
        )
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers))

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class TestPrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="YYY12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "firsttest",
            "last_name": "lasttest",
            "license_number": "TTT12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
