from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse

from taxi.models import Driver


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )

    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_update_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.id]))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )
        self.client.force_login(self.driver)
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="driver123",
            license_number="BBB12345",
        )
        self.driver3 = get_user_model().objects.create_user(
            username="driver3",
            password="driver123",
            license_number="CCC12345",
        )
        self.drivers = Driver.objects.all()

    def test_retrieve_drivers_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(self.drivers))

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver2")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver2")
        self.assertNotContains(response, "driver1")
        self.assertNotContains(response, "driver3")

    def test_driver_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=nonexistent")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(list(response.context["driver_list"]),
                            list(self.drivers))
