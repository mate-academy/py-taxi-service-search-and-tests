from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class DriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="user_admin",
            password="superuser1234",
            license_number="QWE12345"
        )

        self.client.force_login(self.user_admin)

    def test_driver_license_listed(self):
        res = self.client.get(reverse("admin:taxi_driver_changelist"))

        self.assertContains(res, self.user_admin.license_number)

    def test_driver_license_change(self):
        res = self.client.get(
            reverse("admin:taxi_driver_change", args=[self.user_admin.id])
        )

        self.assertContains(res, self.user_admin.license_number)

    def test_driver_fields_add(self):
        res = self.client.get(reverse("admin:taxi_driver_add"))

        self.assertContains(res, "first_name")

        self.assertContains(res, "last_name")

        self.assertContains(res, "license_number")
