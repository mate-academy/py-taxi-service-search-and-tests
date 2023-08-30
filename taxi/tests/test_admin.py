from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminPageTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3"
        )
        self.client.force_login(self.user_admin)

        self.john_smith = get_user_model().objects.create_user(
            username="john_smith",
            password="john_smith77",
            license_number="QWE1234",
            first_name="John",
            last_name="Smith"
        )

    def test_driver_license_number_listed_on_all_drivers(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.john_smith.license_number)

    def test_driver_license_number_listed_on_detail_page(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.john_smith.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.john_smith.license_number)

    def test_driver_license_number_listed_on_addition_page(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "Additional info")
