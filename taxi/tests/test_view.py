from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class DriverSearchTest(TestCase):
    def setUp(self):

        self.driver_ivan = get_user_model().objects.create_user(
            username="ivan_petrov", password="123", license_number="A1"
        )
        self.driver_oleg = get_user_model().objects.create_user(
            username="oleg_ivanov", password="123", license_number="B2"
        )
        self.driver_anna = get_user_model().objects.create_user(
            username="anna_smith", password="123", license_number="C3"
        )

    def test_search_by_username_returns_correct_results(self):
        self.client.force_login(self.driver_ivan)
        res = self.client.get(DRIVER_URL, {"username": "ivan"})
        self.assertEqual(res.status_code, 200)
        drivers = res.context["driver_list"]
        self.assertIn(self.driver_ivan, drivers)
        self.assertIn(self.driver_oleg, drivers)

    def test_search_form_is_in_context(self):
        self.client.force_login(self.driver_ivan)
        response = self.client.get(DRIVER_URL)
        self.assertIn("search_form", response.context)
