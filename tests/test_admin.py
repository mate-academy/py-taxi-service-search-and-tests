from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTestMixin(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="TestUser",
            password="StrongPassword123"
        )
        self.client.force_login(self.admin_user)


class DriverAdminSiteTest(AdminSiteTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.driver = get_user_model().objects.create_superuser(
            username="Driver",
            password="StrongPassword123",
            license_number="ABC12345",
        )

    def test_driver_license_number_change(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_add(self):
        response = self.client.get(reverse("admin:taxi_driver_add"))

        self.assertContains(response, "License number")


class CarAdminSiteTest(AdminSiteTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.car = Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.create(
                name="BMW", country="Germany"
            ),
        )

    def test_car_filter_by_manufacturer(self):
        Car.objects.create(
            model="Celica",
            manufacturer=Manufacturer.objects.create(
                name="Toyota", country="Japan"
            )
        )
        response = self.client.get(reverse("admin:taxi_car_changelist"))
        self.assertContains(response, "By manufacturer")

    def test_search_car_model(self):
        url = reverse(
            "admin:taxi_car_changelist",
        ) + "?q=BMW"
        response = self.client.get(url)

        self.assertNotContains(response, "Toyota")
