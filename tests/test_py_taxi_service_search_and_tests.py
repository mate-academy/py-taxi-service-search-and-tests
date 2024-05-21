from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver

from django.contrib.auth.hashers import make_password


class ManufacturerSearchTestCase(TestCase):
    def setUp(self):
        password = make_password("password")
        self.user = Driver.objects.create(
            username="testuser", password=password
        )

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_manufacturer_search_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)


class DriverSearchTestCase(TestCase):
    def setUp(self):
        password = make_password("password")
        self.user1 = Driver.objects.create(
            username="testuser1",
            password=password,
            first_name="John",
            last_name="Doe",
            license_number="JDO12345",
        )
        self.user2 = Driver.objects.create(
            username="testuser2",
            password=password,
            first_name="Jane",
            last_name="Doe",
            license_number="JAD67890",
        )

    def test_driver_search_by_username(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "testuser2"}
        )
        self.assertEqual(response.status_code, 200)

    def test_driver_search_by_license_number(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse("taxi:driver-list"), {"license_number": "JAD67890"}
        )
        self.assertEqual(response.status_code, 200)
