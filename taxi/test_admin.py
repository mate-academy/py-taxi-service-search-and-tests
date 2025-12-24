from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="<PASSWORD>",
            license_number="TES12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Tesla",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)
        self.car.save()

    def test_admin_driver_license_listed(self):
        """
        Test that driver license is in list_display on driver admin page
        """
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_admin_car_model_search_field(self):
        search_field = "model"
        needed = "Tesla"
        url = reverse(
            "admin:taxi_car_changelist"
        ) + f"?{search_field}={needed}"
        response = self.client.get(url)
        self.assertContains(response, self.car.model)
