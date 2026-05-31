from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "TST12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.check_password(password), True)


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_search_by_model(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="X3", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list"), {"model": "X5"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_search_by_username(self):
        Driver.objects.create_user(
            username="john",
            password="password123",
            license_number="TST12345"
        )
        Driver.objects.create_user(
            username="mike",
            password="password123",
            license_number="TST67890"
        )
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_search_by_name(self):
        Manufacturer.objects.create(name="Tesla")
        Manufacturer.objects.create(name="Toyota")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Tesla"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
