# tests/test_search_django.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer

User = get_user_model()


class SearchTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="driver",
            password="pass",
            license_number="DRIVER001"
        )
        self.client.login(username="driver", password="pass")

    def test_search_driver(self):
        d1 = User.objects.create_user(
            username="john",
            password="pass",
            license_number="DRIVER002"
        )
        d2 = User.objects.create_user(
            username="alex",
            password="pass",
            license_number="DRIVER003"
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"q": "john"})

        self.assertContains(response, d1.username)
        self.assertNotContains(response, d2.username)

    def test_search_car(self):
        man = Manufacturer.objects.create(name="BMW")
        c1 = Car.objects.create(model="X5", manufacturer=man)
        c2 = Car.objects.create(model="Civic", manufacturer=man)

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"q": "X5"})

        self.assertContains(response, c1.model)
        self.assertNotContains(response, c2.model)

    def test_search_manufacturer(self):
        m1 = Manufacturer.objects.create(name="Audi")
        m2 = Manufacturer.objects.create(name="Toyota")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"q": "Audi"})

        self.assertContains(response, m1.name)
        self.assertNotContains(response, m2.name)
