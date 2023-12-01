from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car


class AdminTests(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.driver = Driver.objects.create(
            username="testdriver",
            password="testpassword",
            license_number="XYZ123",
        )

        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_driver_admin_change_page(self):
        self.client.force_login(self.user)
        change_url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver")
        self.assertContains(response, "XYZ123")

    def test_car_admin_change_page(self):
        self.client.force_login(self.user)
        change_url = reverse("admin:taxi_car_change", args=[self.car.id])
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Toyota")

    def test_driver_admin_add_page(self):
        self.client.force_login(self.user)
        add_url = reverse("admin:taxi_driver_add")
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")
        self.assertContains(response, "License number")

    def test_car_admin_add_page(self):
        self.client.force_login(self.user)
        add_url = reverse("admin:taxi_car_add")
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model")
        self.assertContains(response, "Manufacturer")
