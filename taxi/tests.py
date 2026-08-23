from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver.test",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.assertEqual(str(driver), "driver.test (John Doe)")


class PublicAccessTests(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="testpass123",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_manufacturer_search_finds_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        results = response.context["manufacturer_list"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Toyota")

    def test_manufacturer_search_no_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Honda"}
        )
        results = response.context["manufacturer_list"]
        self.assertEqual(len(results), 0)