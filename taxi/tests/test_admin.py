from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="1a2S3r4s5t"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="123driver123",
            license_number="RRR54321"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer,
        )

    def test_drivers_license_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)

    def test_drivers_license_in_additional(self):
        url = reverse("admin:taxi_driver_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertContains(response, self.user.license_number)

    def test_car_in_admin(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
