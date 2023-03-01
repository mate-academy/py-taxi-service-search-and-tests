from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminPanelTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="QWE12345"
        )

    def test_driver_license_number_listed(self):
        """Test that driver's license_number is
        in list_display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_additional_detail_listed(self):
        """Test that driver's license_number, first_name
        and last_name is on driver detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)

    def test_add_driver_additional_detail_listed(self):
        """Test that driver's license_number, first_name
        and last_name is on driver add admin page"""
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "License number")
