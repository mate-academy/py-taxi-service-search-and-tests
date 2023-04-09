from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="test",
            password="testpassword",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="testname",
            password="testpass",
            first_name="firstname",
            last_name="lastname",
            license_number="ABC12345",
        )

    def test_driver_license_number_displayed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_displayed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_create_driver_license_number_displayed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "License number")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
