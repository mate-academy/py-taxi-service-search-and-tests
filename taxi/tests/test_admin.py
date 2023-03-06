from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="Test2",
            password="Test2345",
            license_number="AAA12345"
        )

    def test_driver_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        respond = self.client.get(url)

        self.assertContains(respond, self.driver.license_number)
