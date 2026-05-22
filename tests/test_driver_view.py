from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.driver = Driver.objects.create(
            username="driver_username",
            license_number="ABC12345",
            first_name="driver_first_name",
            last_name="driver_last_name",
        )

    def test_list_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_detail_login_required(self):
        response = self.client.get(DRIVER_URL, {"pk": self.driver.id})
        self.assertNotEquals(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            license_number="ABC12345",
            username="driver_username",
            first_name="driver_first_name",
            last_name="driver_last_name",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            license_number="ABC12345",
            username="driver_username",
            first_name="driver_first_name",
            last_name="driver_last_name",
        )

    def test_driver_search_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "driver_username"})
        self.assertEquals(response.status_code, 200)

        drivers = response.context["driver_list"]
        self.assertEquals(len(drivers), 1)
        self.assertEquals(drivers[0].username, "driver_username")

    def test_driver_search_with_no_result(self):
        response = self.client.get(DRIVER_URL, {"username": "unknown"})
        drivers = response.context["driver_list"]
        self.assertEquals(len(drivers), 0)
