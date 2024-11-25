from django.urls import reverse

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Car, Manufacturer


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="author",
            password="testauthor",
            license_number="TES77777",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver])

    def test_driver_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_detail_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_driver_add_fild_sets_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.first_name)
        self.assertContains(response, self.driver.last_name)
        self.assertContains(response, self.driver.license_number)

    def test_car_search_fild(self) -> None:
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.car.model)

    # def test_car_list_filter_fild(self) -> None:
    #     url = reverse("admin:taxi_car_changelist")
    #     response = self.client.get(url)
    #     self.assertContains(response, self.car.manufacturer)
