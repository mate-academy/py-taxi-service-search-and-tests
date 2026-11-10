from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Admin12345!",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="Driver12345!",
            license_number="ADM56984",
        )

    def test_driver_license_number_listed(self) -> None:
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_page_has_additional_info(self) -> None:
        response = self.client.get(reverse("admin:taxi_driver_add"))
        self.assertContains(response, "Additional info")
        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
