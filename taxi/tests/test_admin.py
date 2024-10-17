from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="TestAdmin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="DriverPass",
            license_number="ABC12345",
            first_name="FirstName",
            last_name="LastName",
        )

    def test_driver_license_number_listed(self) -> None:
        """
        Test that driver's license_number is in
        list_display on driver admin page
        ;return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_licence_number_listed(self) -> None:
        """
        Test that driver's license_number is on detail admin page
        ;return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fields_listed(self) -> None:
        """
        Test that driver's first_name, last_name,
        licence_number display on the page add_fields
        ;return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.pk])
        res = self.client.get(url)
        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
        self.assertContains(res, self.driver.license_number)
