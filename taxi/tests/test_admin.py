from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin_admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="qwe12345",
            license_number="qwe12345"
        )

    def test_driver_license_number_listed(self):
        """Tests that driver`s license number is on driver display"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """Tests that driver`s license number is on driver admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_add_information(self):
        """Tests that driver`s add information is on driver create page"""
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, '<input type="text" name="first_name"')
        self.assertContains(res, '<input type="text" name="last_name"')
        self.assertContains(res, '<input type="text" name="license_number"')

    def test_search_fields_on_the_display(self):
        """Test check is search panel on the car display"""

        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertContains(res, '<input type="search"')
