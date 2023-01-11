from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PrivateDriver(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_two",
            password="test12345"
        )

        self.client.force_login(self.user)

    def test_search_driver(self):
        get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="UA12345"
        )

        get_user_model().objects.create_user(
            username="new_test",
            password="test12345",
            license_number="UA67890"
        )

        search_data = {"username": "test"}
        resp = self.client.get(DRIVER_LIST_URL, data=search_data)
        driver = Driver.objects.filter(username__icontains="test")

        self.assertEqual(
            list(resp.context["driver_list"]),
            list(driver))
