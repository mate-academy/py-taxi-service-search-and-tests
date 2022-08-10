from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        result = self.client.get(CAR_URL)

        self.assertNotEqual(result.status_code, 200)


class PrivateCarTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        test_manufacturer = Manufacturer.objects.create(
            name="Fiat",
            country="Italy",
        )
        Car.objects.create(
            model="Fiesta",
            manufacturer=test_manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
