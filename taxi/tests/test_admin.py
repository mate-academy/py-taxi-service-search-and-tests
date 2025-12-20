from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.admin import CarAdmin


class AdminSiteTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

    def test_admin_page_accessible(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)


class AdminModelRegistrationTest(TestCase):
    def test_car_registered_in_admin(self):
        self.assertIn(Car, admin.site._registry)

    def test_manufacturer_registered_in_admin(self):
        self.assertIn(Manufacturer, admin.site._registry)


class CarAdminTest(TestCase):
    def test_car_admin_list_display(self):
        self.assertEqual(
            CarAdmin.list_display,
            ("model", "manufacturer")
        )

    def test_car_admin_search_fields(self):
        self.assertEqual(
            CarAdmin.search_fields,
            ("model",)
        )

    def test_car_admin_list_filter(self):
        self.assertEqual(
            CarAdmin.list_filter,
            ("manufacturer",)
        )


class AdminCarPageTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )

    def test_car_change_page(self):
        url = reverse("admin:taxi_car_change", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
