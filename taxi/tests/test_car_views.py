from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):

    def test_login_required(self):
        test_response = self.client.get(CAR_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="mypass321"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_retrieve_cars(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        test_response = self.client.get(CAR_URL)
        self.assertEqual(test_response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(test_response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(test_response, "taxi/car_list.html")

    def test_search_car_by_model(self):
        car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

        response = self.client.get(CAR_URL, {"model": "Camry"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(car1, response.context["car_list"])

        response = self.client.get(CAR_URL, {"model": "Cam"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(car1, response.context["car_list"])

        response = self.client.get(CAR_URL, {"model": "Civic"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(car1, response.context["car_list"])
