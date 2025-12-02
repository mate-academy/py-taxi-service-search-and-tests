from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_LIST_URL = reverse("taxi:car-list")


class TestPrivatePage(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="johndoe", password="test123"
        )
        self.client.force_login(self.user)

    def test_login_required(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertEqual(response.status_code, 200)


class TestPublicPage(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="johndoe", password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars_list(self):
        Car.objects.create(
            model="car2",
            manufacturer=Manufacturer.objects.create(name="Tesla")
        )
        Car.objects.create(
            model="car1",
            manufacturer=Manufacturer.objects.create(name="Tesla2")
        )
        response = self.client.get(CARS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")
