from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


class DriverTest(TestCase):
    def setUp(self) -> None:
        self.driver1 = get_user_model().objects.create_user(
            username="stargazer",
            password="nova789#@!",
            first_name="Cassius",
            last_name="Vale",
            license_number="AGX45921"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="windrunner",
            password="storm&cloud77",
            first_name="Thorne",
            last_name="Blackwood",
            license_number="WRN78234"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="shadowrider",
            password="eclipse!2024",
            first_name="Kai",
            last_name="Nakamura",
            license_number="SR98765"
        )
        self.driver4 = get_user_model().objects.create_user(
            username="skypilot",
            password="cosmic$rise",
            first_name="Orion",
            last_name="Drake",
            license_number="SPT34567"
        )
        self.driver5 = get_user_model().objects.create_user(
            username="ravenwatch",
            password="twilight*wing",
            first_name="Aurora",
            last_name="Frost",
            license_number="RVW13579"
        )
        self.client.force_login(self.driver1)

    def test_drivers_without_searching(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Aurora", content)
        self.assertIn("Nakamura", content)
        self.assertIn("WRN78234", content)
        self.assertIn("stargazer", content)

    def test_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "rider"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("shadowrider", content)

    def test_driver_page(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver5.id]))
        self.assertEqual(response.status_code, 200)
