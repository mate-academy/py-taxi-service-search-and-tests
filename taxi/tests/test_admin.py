from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="pass123admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="pass123driver",
            license_number="AAA11111"
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
