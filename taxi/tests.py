from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ManufacturerListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="ABC12345",
        )

        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_manufacturer_list_status_code(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"},
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_manufacturer_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toyota"},
        )

        self.assertContains(response, "Toyota")

    def test_manufacturer_list_without_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")


class CarListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="ABC12345",
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        cls.other_manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

        cls.car1 = Car.objects.create(
            model="Toyota Corolla",
            manufacturer=cls.manufacturer,
        )

        cls.car2 = Car.objects.create(
            model="Ford Focus",
            manufacturer=cls.other_manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_car_list_status_code(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )

        self.assertEqual(response.status_code, 200)

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Corolla"},
        )

        self.assertContains(response, "Toyota Corolla")
        self.assertNotContains(response, "Ford Focus")

    def test_car_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "corolla"},
        )

        self.assertContains(response, "Toyota Corolla")

    def test_car_list_without_search(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )

        self.assertContains(response, "Toyota Corolla")
        self.assertContains(response, "Ford Focus")


class DriverListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="ABC12345",
        )

        cls.driver1 = get_user_model().objects.create_user(
            username="john",
            password="testpassword123",
            license_number="XYZ12345",
        )

        cls.driver2 = get_user_model().objects.create_user(
            username="michael",
            password="testpassword123",
            license_number="DEF12345",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_list_status_code(self):
        response = self.client.get(
            reverse("taxi:driver-list")
        )

        self.assertEqual(response.status_code, 200)

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertContains(response, "john")
        self.assertNotContains(response, "michael")

    def test_driver_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "JOHN"},
        )

        self.assertContains(response, "john")

    def test_driver_list_without_search(self):
        response = self.client.get(
            reverse("taxi:driver-list")
        )

        self.assertContains(response, "john")
        self.assertContains(response, "michael")
