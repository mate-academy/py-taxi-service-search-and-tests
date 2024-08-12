from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="nqpknpks113",
        )
        self.client.force_login(self.user)

    def test_authorised_user_can_access(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="test"
        )
        car1 = Car.objects.create(
            model="Tesla",
            manufacturer=manufacturer,
        )
        car2 = Car.objects.create(
            model="Nissan",
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_LIST_URL)
        queryset = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(queryset)
        )
        self.assertContains(response, car1.model)
        self.assertContains(response, car2.model)
