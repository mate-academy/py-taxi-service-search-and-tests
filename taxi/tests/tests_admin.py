from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Manufacturer, Car


class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            license_number="ADMIN123"
        )
        self.client.force_login(self.admin_user)

    def test_driver_list_page_contains_license_number(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "License number")

    def test_driver_add_page_contains_license_number(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "license_number")

    def test_driver_change_page_contains_license_number(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="pass123",
            license_number="LIC123"
        )
        url = reverse("admin:taxi_driver_change", args=[driver.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "license_number")


class CarAdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin2",
            password="admin123",
            license_number="ADMIN999"
        )
        self.client.force_login(self.admin_user)

    def test_car_list_page(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Model")
