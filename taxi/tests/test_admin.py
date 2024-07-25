from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="client",
            password="client_password",
            license_number="AAA12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test that license_number is in list_display on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver license is in driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_additional_info_in_driver_add(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
        self.assertContains(response, "Additional info")

    def test_manufacturer_is_register_in_admin(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_car_is_register_in_admin(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
