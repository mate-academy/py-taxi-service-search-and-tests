from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")


class PrivateDriverTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for driver_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_user_{driver_id}",
                password="SuperSecretPassword",
                license_number=f"TES1234{driver_id}"
            )

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="SuperSecretPassword",
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self) -> None:
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class SearchDriverViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for driver_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_user_{driver_id}",
                password="SuperSecretPassword",
                license_number=f"TES1234{driver_id}"
            )

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="SuperSecretPassword",
        )
        self.client.force_login(self.driver)

    def test_search_form_returns_filtered_results(self):
        search_param = "?username=driver1"
        response = self.client.get(DRIVER_URL + search_param)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")
