from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Prius", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        expected = (
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(str(driver), expected)


class PublicViewsTests(TestCase):
    def test_login_required_for_lists(self):
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

        self.car_1 = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="A4", manufacturer=self.manufacturer_2
        )

        self.driver_1 = get_user_model().objects.create_user(
            username="speedy_joe",
            password="password123",
            license_number="BBB22222"
        )
        self.driver_2 = get_user_model().objects.create_user(
            username="slow_bob",
            password="password123",
            license_number="CCC33333"
        )

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "tes"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.manufacturer_1, response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer_2, response.context["manufacturer_list"]
        )

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "a4"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car_2, response.context["car_list"])
        self.assertNotIn(self.car_1, response.context["car_list"])

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "joe"})
        self.assertEqual(response.status_code, 200)

        drivers_in_context = list(response.context["driver_list"])
        self.assertIn(self.driver_1, drivers_in_context)
        self.assertNotIn(self.driver_2, drivers_in_context)
