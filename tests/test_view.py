from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTaxiTests(TestCase):
    def test_list_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_page_status_code(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_page_status_code(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
            license_number="AAA55555"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="test"
        )
        self.car = Car.objects.create(
            model="test", manufacturer=self.manufacturer
        )
        self.user.cars.add(self.car)
        self.client.force_login(self.user)

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")


class ToggleViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="password", license_number="AAA55555"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="UK"
        )
        self.car = Car.objects.create(
            model="test", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_toggle_car_assign(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertFalse(self.car in self.user.cars.all())
        another_user = get_user_model().objects.create_user(
            username="user",
            password="password",
            license_number="ABC12312",
        )
        self.client.force_login(another_user)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertTrue(self.car in another_user.cars.all())
