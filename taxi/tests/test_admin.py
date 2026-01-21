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
        self.driver = get_user_model().objects.create_superuser(
            username="olesshulzh",
            password="2405",
            first_name="Oles",
            last_name="Shulzhenko",
            license_number="OSh240596"
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver's license_number is in list_display
        on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver's license_number is in list_display
        on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fieldsets(self):
        """
        Test that driver's first_name, last_name, license_number
        is in add_fieldsets on driver add admin page
        :return:
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, 'name="first_name"')
        self.assertContains(res, 'name="last_name"')
        self.assertContains(res, 'name="license_number"')
