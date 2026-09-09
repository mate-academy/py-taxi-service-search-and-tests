from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.driver1 = Driver.objects.create_user(
            username="test_driver",
            password="test1234",
            license_number="ISA12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="another_driver",
            password="test4321",
            license_number="ISA98765"
        )

    def test_driver_search_finds_existing_driver(self):
        url = reverse("taxi:driver-list") + "?username=test"
        response = self.client.get(url)

        self.assertContains(response, "test_driver")
        self.assertNotContains(response, "another_driver")

    def test_driver_search_returns_all_when_empty(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertContains(response, "test_driver")
        self.assertContains(response, "another_driver")

    def test_driver_search_finds_nothing(self):
        url = reverse("taxi:driver-list") + "?username=nonexistent"
        response = self.client.get(url)

        self.assertNotContains(response, "test_driver")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="another_manufacturer", country="test_country2"
        )

    def test_manufacturer_search_finds_existing_driver(self):
        url = reverse("taxi:manufacturer-list") + "?name=test"
        response = self.client.get(url)

        self.assertContains(response, "test_manufacturer")
        self.assertNotContains(response, "another_manufacturer")

    def test_manufacturer_search_returns_all_when_empty(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertContains(response, "test_manufacturer")
        self.assertContains(response, "another_manufacturer")

    def test_manufacturer_search_finds_nothing(self):
        url = reverse("taxi:manufacturer-list") + "?name=nonexistent"
        response = self.client.get(url)

        self.assertNotContains(response, "test_manufacturer")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

        manufacturer1 = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="test_manufacturer2", country="test_country2"
        )
        self.car1 = Car.objects.create(
            model="test_car", manufacturer=manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="another_car", manufacturer=manufacturer2,
        )

    def test_car_search_finds_existing_driver(self):
        url = reverse("taxi:car-list") + "?model=test"
        response = self.client.get(url)

        self.assertContains(response, "test_car")
        self.assertNotContains(response, "another_car")

    def test_car_search_returns_all_when_empty(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertContains(response, "test_car")
        self.assertContains(response, "another_car")

    def test_car_search_finds_nothing(self):
        url = reverse("taxi:car-list") + "?model=nonexistent"
        response = self.client.get(url)

        self.assertNotContains(response, "test_car")
