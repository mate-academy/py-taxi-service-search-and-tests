from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin_test",
            password="12345admin"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="driver_test",
            password="12345driver",
            license_number="1234"
        )

    def test_driver_detail_license_listed(self):
        response = self.client.get(
            reverse(
                "admin:taxi_driver_change",
                args=(self.driver.id,)
            )
        )
        self.assertContains(response, self.driver.license_number)

    def test_add_driver_detail_license(self):
        response = self.client.get(
            reverse(
                "admin:taxi_driver_add"
            )
        )
        self.assertContains(response, "License number")
