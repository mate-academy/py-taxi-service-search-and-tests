from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class BaseCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3"
        )
        self.client.login(username="test_user", password="1qazcde3")


class ManufacturerSearchTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Citroën",
            country="France"
        )

    def test_manufacturer_search_full_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Audi"})
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "Citroën")

    def test_manufacturer_search_piece_of_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "ud"})
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "Citroën")

    def test_manufacturer_search_empty_field(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertContains(response, "Audi")
        self.assertContains(response, "Citroën")


class CarSearchTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.car1 = Car.objects.create(
            model="A4",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="RS6",
            manufacturer=self.manufacturer
        )

    def test_car_search_full_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "A4"})
        self.assertContains(response, "A4")
        self.assertNotContains(response, "RS6")

    def test_car_search_piece_of_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "4"})
        self.assertContains(response, "A4")
        self.assertNotContains(response, "RS6")

    def test_car_search_empty_field(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertContains(response, "A4")
        self.assertContains(response, "RS6")


class DriverSearchTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.driver1 = Driver.objects.create_user(
            username="test_driver",
            password="123qweasdzxc",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="tom_wilson",
            password="zxcasdqwe123",
            license_number="XYZ67890"
        )

    def test_driver_search_full_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "test_driver"})
        self.assertContains(response, "test_driver")
        self.assertNotContains(response, "tom_wilson")

    def test_driver_search_piece_of_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "wilson"})
        self.assertContains(response, "tom_wilson")
        self.assertNotContains(response, "test_driver")

    def test_driver_search_empty_field(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertContains(response, "test_driver")
        self.assertContains(response, "tom_wilson")
