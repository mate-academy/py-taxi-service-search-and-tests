from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class DriverAdminPageTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.user_admin)

        self.driver_test = get_user_model().objects.create_user(
            username="user",
            password="user1234",
            license_number="ABD12345",
            first_name="Jimmy",
            last_name="Beam"
        )

    def test_driver_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver_test.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver_test.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.driver_test.license_number)

    def test_driver_detail_first_and_last_name_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver_test.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.driver_test.first_name)
        self.assertContains(res, self.driver_test.last_name)
