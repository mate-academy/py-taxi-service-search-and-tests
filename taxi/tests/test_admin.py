from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1"
        )

        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="Bob",
            password="very_strong_password",
            license_number="QWE45678"
        )
        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car_search_match = Car.objects.create(
            model="Corolla",
            manufacturer=self.toyota
        )

        self.car_filter_match = Car.objects.create(
            model="X5",
            manufacturer=self.bmw
        )

        self.car_no_match = Car.objects.create(
            model="Camry",
            manufacturer=self.toyota
        )

        self.changelist_url = reverse("admin:taxi_car_changelist")

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_create_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "License number")

    def test_search_by_model(self):
        response = self.client.get(self.changelist_url, {"q": "rolla"})

        self.assertContains(response, self.car_search_match.model)
        self.assertNotContains(response, self.car_filter_match.model)
        self.assertNotContains(response, self.car_no_match.model)

    def test_filter_by_manufacturer(self):
        filter_params = {"manufacturer__id__exact": self.bmw.id}
        response = self.client.get(self.changelist_url, filter_params)

        self.assertContains(response, self.car_filter_match.model)

        self.assertNotContains(response, self.car_search_match.model)
        self.assertNotContains(response, self.car_no_match.model)

        self.assertContains(response, "Manufacturer")
