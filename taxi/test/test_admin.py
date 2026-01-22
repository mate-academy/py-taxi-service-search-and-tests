from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            first_name="Chan",
            last_name="Li",
            password="driver",
            license_number="ABC71787"
        )

    def test_driver_license_number_listed(self):
        """
        Test get driver`s license number is in
        list_display on driver admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test get driver`s license number is on driver detail admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_add(self):
        """
        Test check to add driver`s license number on driver detail admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, 'name="license_number"')
