from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="testadminpassword"
        )
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="testuserpassword",
            license_number="ABC12345"
        )

    def test_driver_license_listed_on_admin_page(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        test_response = self.client.get(url)
        self.assertContains(test_response, self.driver.license_number)

    def test_driver_license_listed_on_driver_details(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        test_response = self.client.get(url)
        self.assertContains(test_response, self.driver.license_number)

    def test_driver_add_license_number_in_add_driver_page(self) -> None:
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")
