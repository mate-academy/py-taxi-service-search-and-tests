from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import admin

from taxi.models import Driver, Car
from ..admin import DriverAdmin, CarAdmin


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="TestAdmin",
            email="admin@example.com",
            password="Test123321#",
        )
        self.client.force_login(self.admin_user)

    def test_driver_admin_display(self):
        driver_admin = DriverAdmin(Driver, admin.site)
        self.assertEqual(driver_admin.list_display, (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "license_number"
        )
        )

    def test_car_admin_search(self):
        car_admin = CarAdmin(Car, admin.site)
        self.assertEqual(car_admin.search_fields, ("model",))

    def test_manufacturer_registered(self):
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "Manufacturer")

    def test_driver_add_page(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))
        self.assertEqual(response.status_code, 200)

    def test_driver_license(self):
        driver = Driver.objects.create(
            license_number="XML00000"
        )
        url = reverse("admin:taxi_driver_change", args=[driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "license_number")
