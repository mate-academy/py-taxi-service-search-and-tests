from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_admin = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
        )
        self.client.force_login(self.user_admin)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testDriver",
            license_number="HGF78790",
        )

    def test_driver_license_field(self):
        """
            Testing if the driver license field
            is presented at admin page
            :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_field(self):
        """
            Testing if the driver license field
            is presented at driver detail page
            :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_addition_info_fieldset(self):
        """
            Testing if the addition info fieldset
            is presented at driver detail page
            :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)
