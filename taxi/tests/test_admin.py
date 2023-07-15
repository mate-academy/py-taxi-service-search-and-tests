from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123456"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123456",
            license_number="LIS123456"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test Kingdom"
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_created_additional_info_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")

    def test_car_filter_by_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1 manufacturer",
            country="Test Kingdom"
        )

        Car.objects.create(
            model="Test model1",
            manufacturer=manufacturer
        )

        url = reverse(
            "admin:taxi_car_changelist",
        )
        response = self.client.get(url)

        self.assertContains(response, "By manufacturer")

    def test_search_car_model(self):
        Car.objects.create(
            model="Test new car",
            manufacturer=self.manufacturer
        )

        url = reverse(
            "admin:taxi_car_changelist",
        ) + "?q=new"
        response = self.client.get(url)

        self.assertNotContains(response, "Test model")
