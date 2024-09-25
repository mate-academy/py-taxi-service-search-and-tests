from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_name", password="test_123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="driver_123",
            license_number="DRV12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Nissan", country="Japan"
        )
        self.car = Car.objects.create(
            model="Skyline", manufacturer=self.manufacturer
        )

    def test_license_number_in_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, "DRV12345")

    def test_license_number_in_fieldsets(self):
        url = reverse(
            "admin:taxi_driver_change", args=[self.driver.id]
        )
        response = self.client.get(url)
        self.assertContains(response, "License number")

    def test_car_model_in_list_display(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Skyline")

    def test_manufacturer_in_list_display(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Manufacturer")
