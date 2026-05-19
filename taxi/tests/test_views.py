from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class PublicViewsTest(TestCase):
    """Unauthenticated users should be redirected to login."""

    def test_manufacturer_list_requires_login(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_requires_login(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_requires_login(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_accessible(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_accessible(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_accessible(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
