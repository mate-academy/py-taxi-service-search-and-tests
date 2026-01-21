from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="25qwerty1",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test.user",
            password="25qwerty1",
            license_number="AAA12345"
        )

    def test_license_number_in_driver_changelist(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_license_number_in_driver_change(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_additional_info_fields_in_driver_add(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "license_number")
        self.assertContains(response, "Additional info")


class AdminSiteManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="25qwerty1",
        )
        self.client.force_login(self.admin_user)

    def test_manufacturer_is_register_in_admin(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class AdminSiteCarTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="25qwerty1",
        )
        self.client.force_login(self.admin_user)

    def test_car_is_register_in_admin(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
