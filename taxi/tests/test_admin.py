from django.urls import reverse

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Car, Manufacturer


class AdminSiteCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="email@email.com",
            username="adminuser",
            password="password"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            email="<EMAIL>",
            username="testdriver",
            password="password1",
            license_number="AAA12345"
        )
        self.manufacturer_first = Manufacturer.objects.create(
            name="First Manufacturer",
            country="First Country",
        )
        self.manufacturer_second = Manufacturer.objects.create(
            name="Second Manufacturer",
            country="Second Country",
        )
        self.car_first = Car.objects.create(
            model="FirstModel",
            manufacturer=self.manufacturer_first,
        )
        self.car_second = Car.objects.create(
            model="SecondModel",
            manufacturer=self.manufacturer_second,
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_listed_in_fieldsets(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_car_list_admin_has_search_by_model(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"),
            {"q": "FirstModel"}
        )
        self.assertContains(response, self.car_first.model)
        self.assertNotContains(response, self.car_second.model)

    def test_car_list_has_filter_by_manufacturer(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"),
            {"manufacturer__id": self.manufacturer_first.id}
        )
        self.assertContains(response, "FirstModel")
        self.assertNotContains(response, "SecondModel")
