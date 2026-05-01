from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password123",
            license_number="ADM00000"
        )
        self.client.force_login(self.admin_user)

        self.manufacturer: Manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.car: Car = Car.objects.create(
            model="Model 3", manufacturer=self.manufacturer
        )

    def test_driver_admin_list_display(self) -> None:

        url: str = reverse("admin:taxi_driver_changelist")
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.admin_user.license_number)

    def test_driver_admin_add_fieldsets(self) -> None:
        url: str = reverse("admin:taxi_driver_add")
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "license_number")

    def test_driver_admin_change_fieldsets(self) -> None:
        url: str = reverse(
            "admin:taxi_driver_change",
            args=[self.admin_user.id]
        )
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "license_number")

    def test_car_admin_list_display_and_filters(self) -> None:
        url: str = reverse("admin:taxi_car_changelist")
        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
