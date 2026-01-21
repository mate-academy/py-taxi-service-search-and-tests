from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AdminPanelTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="Test123",
            first_name="Test first",
            last_name="Test last",
            license_number="TST12345",
        )

    def test_manufacturer_list_display(self) -> None:
        url = reverse("admin:taxi_manufacturer_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.manufacturer.name,)

    def test_manufacturer_detail_display(self) -> None:
        url = reverse(
            "admin:taxi_manufacturer_change",
            args=[self.manufacturer.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.manufacturer.name,)

    def test_car_list_display(self) -> None:
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.car.model,)

    def test_car_detail_display(self) -> None:
        url = reverse(
            "admin:taxi_car_change",
            args=[self.car.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.car.model,)

    def test_driver_list_display(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_display(self) -> None:
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.driver.id],
        )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)
