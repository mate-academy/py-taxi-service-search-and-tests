from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicTaxiTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateTaxiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            license_number="AAA11111"
        )
        self.client.login(username="test.user", password="password123")
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )

    def test_retrieve_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tesla")

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "tes"}
        )
        self.assertContains(res, "Tesla")
        self.assertNotContains(res, "Toyota")

    def test_car_search_by_model(self):
        Car.objects.create(model="Model S", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        res = self.client.get(reverse("taxi:car-list"), {"model": "model"})
        self.assertContains(res, "Model S")
        self.assertNotContains(res, "Camry")

    def test_driver_search_by_username(self):
        get_user_model().objects.create_user(
            username="other.driver",
            password="password123",
            license_number="BBB22222"
        )
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )
        self.assertContains(res, "test.user")
        self.assertNotContains(res, "other.driver")

    def test_car_detail_page_contains_manufacturer(self):
        car = Car.objects.create(
            model="Model X",
            manufacturer=self.manufacturer
        )
        url = reverse("taxi:car-detail", kwargs={"pk": car.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tesla")
