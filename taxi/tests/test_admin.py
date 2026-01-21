from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="testauthor",
            license_number="TES12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test that drivers license_number is in list_display
        on driver admin page
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that drivers license_number is on driver detail admin page
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_license_number_in_add_fieldsets(self):
        """
        Test that the 'license_number' field is in the add_fieldsets
        on the add driver admin page
        """
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        self.assertContains(res, "license_number")
