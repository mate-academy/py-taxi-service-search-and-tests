from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="AAA12345",
        )

    def test_driver_license_number_is_present(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
