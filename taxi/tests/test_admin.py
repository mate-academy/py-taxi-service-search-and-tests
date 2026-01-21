from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="adminuser",
            password="adminpassword"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driverpassword",
            license_number="ATN12345"
        )

    def test_driver_license_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)
