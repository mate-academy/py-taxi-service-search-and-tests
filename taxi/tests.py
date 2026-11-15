from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_user",
            password="pass12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.toyota = Manufacturer.objects.create(name="Toyota",
                                                  country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Corolla", manufacturer=self.toyota)
        Car.objects.create(model="Mustang",
                           manufacturer=Manufacturer.objects.get(name="Ford"))

    def test_manufacturer_search(self):
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              {"name": "toy"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Ford")

    def test_car_search(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "must"})
        self.assertContains(res, "Mustang")
        self.assertNotContains(res, "Corolla")

    def test_driver_search(self):
        res = self.client.get(reverse("taxi:driver-list"),
                              {"username": "admin"})
        self.assertContains(res, "admin_user")

    def test_empty_search_returns_all(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertEqual(len(res.context["car_list"]), 2)
