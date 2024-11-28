from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin", password="1234"
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="1234",
            license_number="QWE12345",
        )

    def test_license_number_displayed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        result = self.client.get(url)
        self.assertContains(result, "QWE12345")
