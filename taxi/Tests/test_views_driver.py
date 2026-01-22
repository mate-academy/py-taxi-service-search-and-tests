from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

DRIVER_FORMAT_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_drivers(self):
        Driver.objects.create(
            username="driver1",
            license_number="BNM12345"
        )
        Driver.objects.create(
            username="driver2",
            license_number="MKB54321"
        )
        response = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(
            response.status_code, 200
        )
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )
