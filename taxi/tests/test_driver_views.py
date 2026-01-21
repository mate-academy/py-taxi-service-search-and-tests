from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self) -> None:
        test_response = self.client.get(DRIVER_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver1 = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword"
        )
        self.client.force_login(self.driver1)

    def test_retrieve_driver_list(self) -> None:
        test_response = self.client.get(DRIVER_URL)
        self.assertEqual(test_response.status_code, 200)
        all_drivers = Driver.objects.all()
        self.assertEqual(all_drivers.count(), 1)
        self.assertTemplateUsed(test_response, "taxi/driver_list.html")
