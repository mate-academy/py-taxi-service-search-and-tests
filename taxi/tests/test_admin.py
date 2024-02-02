from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpass"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="testpass",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="SSS22222"
        )

    def test_license_number_field_in_driver_list(self):
        """
        Test that license number is in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_license_number_field_in_driver_detail(self):
        """
            Test that license number is in fieldsets on driver info admin page
        """
        url = reverse(
            "admin:taxi_driver_change",
            kwargs={"object_id": self.driver.id}
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_license_number_field_in_add_driver_page(self):
        """
            Test that license number
            is in add_fieldsets on driver add admin page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "license_number")
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
