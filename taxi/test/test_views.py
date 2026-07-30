from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class ViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="john",
            password="password",
            license_number="ABC12345"
        )

    def test_index_requires_login(self):
        response = self.client.get(
            reverse("taxi:index")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_index_logged_user(self):
        self.client.login(
            username="john",
            password="password"
        )

        response = self.client.get(
            reverse("taxi:index")
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertIn(
            "num_drivers",
            response.context
        )
