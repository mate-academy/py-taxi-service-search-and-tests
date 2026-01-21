from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverViewTest(TestCase):
    def test_login_required(self):
        """
        Test that login is required to access the driver page
        """
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        """
        Test that login is required to access the driver page
        """
        Driver.objects.create(
            username="test_username_1",
            license_number="ABC12345",
        )
        Driver.objects.create(
            username="test_username_2",
            license_number="XYZ67890",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )
