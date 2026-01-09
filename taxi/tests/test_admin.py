from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="pass321",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test.user",
            license_number="XYZ12345"
        )

    def test_driver_license_number_listed(self):
        """
        Test driver's that license_number is in drivers list on admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_detail(self):
        """
        Test driver's that license_number is in change view on admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_in_add_user(self):
        """
        Test driver's license_number field is in add user on admin page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "License number:")
