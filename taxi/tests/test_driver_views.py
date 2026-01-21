from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):

    def test_login_required(self):
        test_response = self.client.get(DRIVER_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="mypass321"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(username="driver1", license_number="XYZ123")
        Driver.objects.create(username="driver2", license_number="ABC456")
        test_response = self.client.get(DRIVER_URL)
        self.assertEqual(test_response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(test_response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(test_response, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        driver1 = Driver.objects.create(
            username="driver1",
            license_number="XYZ123"
        )

        response = self.client.get(DRIVER_URL, {"username": "driver1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(driver1, response.context["driver_list"])

        response = self.client.get(DRIVER_URL, {"username": "driver"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(driver1, response.context["driver_list"])

        response = self.client.get(DRIVER_URL, {"username": "notfound"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(driver1, response.context["driver_list"])
