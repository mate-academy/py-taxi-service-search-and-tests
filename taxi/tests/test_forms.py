from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class DriverSearchTests(TestCase):
    def setUp(self):
        self.url = reverse("taxi:driver-list")
        self.matching_driver = get_user_model().objects.create(
            username="speedy_gonzales",
            password="test_password",
            first_name="first_name",
            last_name="last_name",
            license_number="NBV12345"
        )
        self.other_driver = get_user_model().objects.create(
            username="slow_bob",
            password="test_password",
            first_name="first_name",
            last_name="last_name",
            license_number="IKJ12345"
        )
        self.client.force_login(self.matching_driver)

    def test_search_by_username_returns_correct_driver(self):
        response = self.client.get(self.url, {"username": "speedy"})
        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]

        self.assertIn(self.matching_driver, driver_list)
        self.assertNotIn(self.other_driver, driver_list)

    def test_search_with_no_results(self):
        response = self.client.get(self.url, {"username": "non_existent_user"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)


class CarSearchTests(TestCase):
    def setUp(self):
        self.model = "test_model"
        self.url = reverse("taxi:car-list")
        self.manufacturer = Manufacturer.objects.create(
            name="Test_Name",
            country="Test_Country"
        )
        self.car = Car.objects.create(
            model=self.model,
            manufacturer=self.manufacturer,
        )
        self.user = get_user_model().objects.create(
            username="speedy_gonzales",
            password="test_password",
            first_name="first_name",
            last_name="last_name",
            license_number="NBV12345"
        )

        self.client.force_login(self.user)

    def test_search_by_car_returns_correct_car(self):
        response = self.client.get(self.url, {"model": self.model})
        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]

        self.assertIn(self.car, car_list)

    def test_search_with_no_results(self):
        response = self.client.get(self.url, {"model": "non_existent_model"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.name = "Test_Name"
        self.country = "Test_Country"
        self.url = reverse("taxi:manufacturer-list")
        self.manufacturer = Manufacturer.objects.create(
            name=self.name,
            country=self.country
        )
        self.user = get_user_model().objects.create(
            username="speedy_gonzales",
            password="test_password",
            first_name="first_name",
            last_name="last_name",
            license_number="NBV12345"
        )

        self.client.force_login(self.user)

    def test_search_by_manufacturer_returns_correct_manufacturer(self):
        response = self.client.get(self.url, {"name": self.name})
        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer, manufacturer_list)

    def test_search_with_no_results(self):
        response = self.client.get(self.url, {"name": "non_existent_name"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 0)
