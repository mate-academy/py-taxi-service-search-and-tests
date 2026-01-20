from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver_pass",
            license_number="Test license number"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        self.car = Car.objects.create(
            model="Test car model",
            manufacturer=self.manufacturer
        )

    def test_driver_license_number_listed(self):
        """Tests that driver's license number is in list_display on
        driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_add_first_and_last_names(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)

    def test_manufacturer_list_page(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.manufacturer)

    def test_car_list_page(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.car)
