from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver", password="testdriver", license_number="QQQ12345"
        )

    def test_driver_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_create_page(self) -> None:
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_change_page(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
