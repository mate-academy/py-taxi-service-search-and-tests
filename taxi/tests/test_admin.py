from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class DriverAdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="qwerty"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="asdf",
            license_number="ZXC12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_add_license_number_listed(self):
        url = reverse("admin:taxi_driver_add")
        response = self.client.get(url)

        self.assertContains(response, "license_number")


class CarAdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="qwerty"
        )
        self.client.force_login(self.admin_user)

        manufacturer = Manufacturer.objects.create(
            name="Audi Motors",
            country="German"
        )
        driver = get_user_model().objects.create_user(
            username="Carl",
            password="qwerty",
            license_number="ZXC12345"
        )
        self.car = Car.objects.create(model="BMW", manufacturer=manufacturer)
        self.car.drivers.set([driver])

    def test_car_model_listed(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.car.model)

    def test_car_manufacturer_list_filter(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "manufacturer")

    def test_car_model_search_field(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)
        self.assertContains(response, "model")

    def test_car_add_has_model_field(self):
        url = reverse("admin:taxi_car_add")
        response = self.client.get(url)
        self.assertContains(response, "model")

    def test_car_add_has_manufacturer_field(self):
        url = reverse("admin:taxi_car_add")
        response = self.client.get(url)
        self.assertContains(response, "manufacturer")

    def test_car_add_has_drivers_field(self):
        url = reverse("admin:taxi_car_add")
        response = self.client.get(url)
        self.assertContains(response, "drivers")
