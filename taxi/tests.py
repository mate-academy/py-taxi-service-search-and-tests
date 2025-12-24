from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
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
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(
            model="glc",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class SearchFormTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create(
            username="test",
            password="test123",
        )
        self.client.force_login(self.admin_user)

    def test_search_form_manufacturer(self):
        first_manufacturer = Manufacturer.objects.create(name="test",
                                                         country="test")
        second_manufacturer = Manufacturer.objects.create(name="fake",
                                                          country="fake")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "test"})
        results = response.context["manufacturer_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
        self.assertIn(first_manufacturer, results)
        self.assertNotIn(second_manufacturer, results)

    def test_search_form_driver(self):
        driver = get_user_model().objects.create(
            username="John",
            password="JohnJohn",
            first_name="John",
            last_name="Johny",
            license_number="ABC23456",
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "test"})
        results = response.context["driver_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
        self.assertIn(self.admin_user, results)
        self.assertNotIn(driver, results)

    def test_search_form_car(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car1 = Car.objects.create(
            model="glc",
            manufacturer=manufacturer
        )

        car2 = Car.objects.create(
            model="focus",
            manufacturer=manufacturer
        )

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "glc"})
        results = response.context["car_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 1)
        self.assertIn(car1, results)
        self.assertNotIn(car2, results)
