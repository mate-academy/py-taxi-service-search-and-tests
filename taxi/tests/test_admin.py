from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestAdmin(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="password12"
        )
        self.client = Client()
        self.client.force_login(self.admin)
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="password123",
            license_number="ABC45678"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="USA"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

    def test_license_number_listed_on_admin_page(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_license_number_listed_on_detail_admin_page(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_car_search_fields(self):

        url = reverse("admin:taxi_car_changelist") + "?q=test_model"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_model")

    def test_list_filter(self):
        response = self.client.get(reverse(
            "admin:taxi_car_changelist"),
            {"manufacturer__exact": self.manufacturer}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "admin:taxi_car_changelist") + f"?e={self.manufacturer.id}"
        )
