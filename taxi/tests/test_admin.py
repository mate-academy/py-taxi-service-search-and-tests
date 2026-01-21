from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",

        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="<PASSWORD>",
            license_number="123456789"
        )

    def test_driver_license_number_listed(self):
        """
        Test get driver license number listed.
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)


class CarAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",
        )
        self.client.force_login(self.admin_user)

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="US"
        )
        self.car = Car.objects.create(
            model="model",
            manufacturer=self.manufacturer,
        )

    def test_car_model_search(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"q": "model"})
        self.assertContains(res, self.car.model)

    def test_car_list_filter_by_manufacturer(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url, {"manufacturer__id__exact": self.car.manufacturer.id})
        self.assertContains(res, self.car.model)
