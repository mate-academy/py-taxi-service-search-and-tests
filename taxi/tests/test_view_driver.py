from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self) -> None:
        test_response = self.client.get(DRIVER_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self) -> None:
        test_response = self.client.get(DRIVER_URL)
        self.assertEqual(test_response.status_code, 200)
        all_drivers = Driver.objects.all()
        self.assertEqual(all_drivers.count(), 1)
        self.assertTemplateUsed(test_response, "taxi/driver_list.html")
