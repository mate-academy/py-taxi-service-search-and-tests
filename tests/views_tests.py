from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car

URL_TAXI = reverse("taxi:car-list")


class PublicTaxiTests(TestCase):
    def test_login_required(self):
        res = self.client.get(URL_TAXI)
        self.assertEqual(res.status_code, 302)


class PrivateTaxiTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_taxi(self):
        Car.objects.create(model="Toyota")
        Car.objects.create(model="BMW")
        response = self.client.get(URL_TAXI)
        self.assertEqual(response.status_code, 200)
        taxi = Car.objects.all()
        self.assertEqual(response.context["car_list "], taxi)
