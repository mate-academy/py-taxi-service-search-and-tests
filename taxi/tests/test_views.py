from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)
        self.test_manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US")

    def test_retrieve_cars(self):
        Car.objects.create(model="testmodel",
                           manufacturer=self.test_manufacturer)
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
