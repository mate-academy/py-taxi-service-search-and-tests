from django.urls import reverse

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin", password="<PASSWORD>")
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="<PASSWORD>", license_number="ADF12345"
        )

    def test_driver_detail_license_listed(self):
        response = self.client.get(
            reverse(
                "admin:taxi_driver_change",
                args=[self.driver.id]
            )
        )
        self.assertContains(response, self.driver.license_number)
