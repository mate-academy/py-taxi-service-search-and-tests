from django.contrib.auth import get_user_model

from django.test import TestCase

from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PrivateDriver(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test2",
            password="test21232"
        )

        self.client.force_login(self.user)

    def test_search_driver(self):
        get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="TEST234"
        )

        get_user_model().objects.create_user(
            username="new",
            password="test12345",
            license_number="TET234"
        )

        search_data = {"username": "test"}
        resp = self.client.get(DRIVER_LIST_URL, data=search_data)
        driver = Driver.objects.filter(username__icontains="test")

        self.assertEqual(
            list(resp.context["driver_list"]),
            list(driver)
        )
