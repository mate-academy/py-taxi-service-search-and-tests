from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class PublicViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            license_number="TEST99999"
        )
        self.client.force_login(self.driver)
        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="Tesla", country="USA")

    def test_search_manufacturer_by_name(self):
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              {"name": "yota"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Tesla")

    def test_search_car_by_model(self):
        Car.objects.create(model="Camry", manufacturer=self.m1)
        Car.objects.create(model="Model S", manufacturer=self.m2)
        res = self.client.get(reverse("taxi:car-list"), {"model": "amry"})
        self.assertContains(res, "Camry")
        self.assertNotContains(res, "Model S")

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="driver.one",
            password="password123",
            license_number="AAA11111"
        )
        get_user_model().objects.create_user(
            username="driver.two",
            password="password123",
            license_number="BBB22222"
        )
        res = self.client.get(reverse("taxi:driver-list"), {"username": "one"})
        self.assertContains(res, "driver.one")
        self.assertNotContains(res, "driver.two")
