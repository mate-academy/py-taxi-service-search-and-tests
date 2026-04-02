from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class SearchAndPaginationTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            license_number="ABC11111"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        for i in range(8):
            Manufacturer.objects.create(
                name=f"Brand {i}",
                country="Germany"
            )

        for i in range(8):
            Car.objects.create(
                model=f"Camry {i}",
                manufacturer=self.manufacturer
            )

        for i in range(8):
            User.objects.create_user(
                username=f"driver_{i}",
                password="password123",
                license_number=f"DRIVER_{i}"
            )

    def test_drivers_search_logic(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"q": "driver"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 5)
        self.assertEqual(response.context["paginator"].count, 8)
        self.assertIn("search_form", response.context)
        self.assertContains(response, 'value="driver"')

    def test_cars_search_logic(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"q": "camry"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertContains(response, 'value="camry"')
        self.assertContains(response, "q=camry")
        self.assertContains(response, "page=2")

    def test_manufacturers_search_logic(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"q": "BRAND"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertContains(response, 'value="BRAND"')

    def test_empty_search_returns_all_results(self):
        self.client.login(username="testuser", password="password123")
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list")
        ]
        for url in urls:
            response = self.client.get(url, {"q": ""})
            self.assertEqual(response.status_code, 200)
            keys = response.context.keys()
            target = next(iter(keys & {
                "driver_list",
                "car_list",
                "manufacturer_list"
            }))
            self.assertEqual(len(response.context[target]), 5)

    def test_anonymous_user_redirect(self):
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list")
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"/accounts/login/?next={url}")
