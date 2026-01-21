from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="testuser",
            password="<PASSWORD>",
        )
        Driver.objects.create_user(
            username="God",
            first_name="john",
            last_name="Jonson",
            license_number="ADS13245"
        )
        Driver.objects.create_user(
            username="Devil",
            first_name="Bob",
            last_name="Bobson",
            license_number="SDG23456"
        )
        Driver.objects.create_user(
            username="Angel",
            first_name="Jack",
            last_name="Jackson",
            license_number="JKL34567"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_context(self):
        response = self.client.get(DRIVER_URL)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertIn("search_form", response.context)

    def test_list_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "God")
        self.assertContains(response, "Devil")
        self.assertContains(response, "Angel")

    def test_driver_search_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "go"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "God")
        self.assertNotContains(response, "Devil")
        self.assertNotContains(response, "Angel")

    def test_driver_search_with_no_match(self):
        response = self.client.get(DRIVER_URL, {"username": "dem"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "God")
        self.assertNotContains(response, "Devil")
        self.assertNotContains(response, "Angel")
        self.assertContains(response,
                            "There are no drivers in the service.",
                            html=True)
