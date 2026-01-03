from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestCarSearchForm(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Manuf1",
            country="CTest"
        )
        self.car1 = Car.objects.create(
            model="Mode1",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Mode2",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create(
            username="driver1",
            password="pass123",
            first_name="Driver",
            last_name="One",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.car1.drivers.add(self.driver)
        self.car2.drivers.add(self.driver)

    def test_search_model(self) -> None:
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "Mode1"})
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test1",
            country="country1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test2",
            country="country2"
        )
        self.driver = get_user_model().objects.create(
            username="driver1",
            password="pass123",
            first_name="Driver",
            last_name="One",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_search_exact_name(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "Test1"})
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)


class TestDriverSearchForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass123",
        )
        self.client.force_login(self.user)
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="pass123",
            first_name="Driver",
            last_name="One",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="pass123",
            first_name="Driver",
            last_name="Two",
            license_number="DEF67890"
        )

    def test_search_exact_username(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "driver1"})
        self.assertIn(self.driver1, response.context.get("driver_list"))
        self.assertNotIn(self.driver2, response.context.get("driver_list"))
