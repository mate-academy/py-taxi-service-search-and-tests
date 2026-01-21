from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="ABC12345",
        )

    def test_driver_license_number_listed(self):
        """
        Test that driver license_number is in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        """
        Test that driver license_number is on driver detail admin page
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_create_license_number_listed(self):
        """
        Test that driver license_number is on driver create admin page
        """
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")

    def test_car_model_search_fields(self):
        """
        Test existing the search field on car admin page
        """
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Search")

    def test_car_model_filter_fields(self):
        """
        Test existing the list filter on car admin page
        """
        url = reverse("admin:taxi_car_changelist")
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Test country"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Test2", country="Test country2"
        )
        response = self.client.get(url)
        self.assertContains(response, manufacturer.name)
        self.assertContains(response, manufacturer2.name)
