from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


CARS_LIST_URL = reverse("taxi:car-list")


class PrivateCarListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Testuser",
            password="Test12345"
        )

        self.client.force_login(self.user)
        manufacturer1 = Manufacturer.objects.create(name="Mercedes")
        manufacturer2 = Manufacturer.objects.create(name="Audi")
        Car.objects.create(model="S600", manufacturer=manufacturer1)
        Car.objects.create(model="A6", manufacturer=manufacturer2)

    def test_retrieve_cars(self):
        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_search_cars(self):
        response = self.client.get(CARS_LIST_URL, {"model": "S600"})
        search_car = Car.objects.filter(model="S600")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(search_car)
        )


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
