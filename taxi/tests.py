from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="ABC12456"
        )
        self.client.force_login(self.user)

    def test_search_manufacturers_by_name(self):
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toy"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(toyota, response.context["manufacturer_list"])
        self.assertNotIn(ford, response.context["manufacturer_list"])

    def test_search_cars_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        civic = Car.objects.create(model="Civic", manufacturer=manufacturer)
        accord = Car.objects.create(model="Accord", manufacturer=manufacturer)
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Civ"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(civic, response.context["car_list"])
        self.assertNotIn(accord, response.context["car_list"])

    def test_search_drivers_by_username(self):
        driver = get_user_model().objects.create_user(
            username="johndoe", password="123", license_number="XYZ98765"
        )
        other = get_user_model().objects.create_user(
            username="admin", password="123", license_number="QWE12345"
        )
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(driver, response.context["driver_list"])
        self.assertNotIn(other, response.context["driver_list"])
