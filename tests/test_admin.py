from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminSiteTestMixin(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)


class DriverAdminSiteTest(AdminSiteTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.driver = get_user_model().objects.create_superuser(
            username="Driver1",
            password="Driver12345!",
            first_name="DriverFirstname",
            last_name="DriverLastname",
            license_number="PVF12345",
        )

    def test_driver_license_number_changelist(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_license_number_change(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_add(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "License number")


class CarAdminSiteTest(AdminSiteTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                name="test_name", country="test_country"
            ),
        )

    def test_car_filter_by_manufacturer(self):
        Car.objects.create(
            model="test_model_2",
            manufacturer=Manufacturer.objects.create(
                name="test_name2", country="test_country2"
            )
        )

        url = reverse("admin:taxi_car_changelist")

        response = self.client.get(url)
        self.assertContains(response, "By manufacturer")

    def test_search_car_model(self):
        url = reverse(
            "admin:taxi_car_changelist",
        ) + "?q=BMW"
        response = self.client.get(url)

        self.assertNotContains(response, "test_model")
