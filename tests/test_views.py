from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ListViewTest(TestCase):
    def login_required(self, url):
        response = self.client.get(reverse(url))
        self.assertNotEqual(response.status_code, 200)


class CarListViewTestCase(ListViewTest):
    def test_login_required(self):
        self.login_required("taxi:driver-list")


class ManufacturerListViewTestCase(ListViewTest):
    def test_login_required(self):
        self.login_required("taxi:manufacturer-list")


class DriverListViewTestCase(ListViewTest):
    def test_login_required(self):
        self.login_required("taxi:driver-list")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="aboba",
            password="<PASSWORD_12345>",
            first_name="Andreww",
            last_name="SS",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="USA"
        )
        self.car = Car.objects.create(
            model="RS6 Avant",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertContains(response, "RS6 Avant")
        self.assertContains(response, self.car.id)

    def test_retrieve_car_detail(self):
        url = reverse("taxi:car-detail", kwargs={"pk": self.car.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertContains(response, self.car.id)
        self.assertContains(response, "USA")
        self.assertContains(response, "RS6 Avant")
