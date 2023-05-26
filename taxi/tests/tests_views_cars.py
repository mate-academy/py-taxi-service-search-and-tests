from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "Kostya",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(model="model_test_1", manufacturer=manufacturer)
        Car.objects.create(model="model_test_2", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(model="model_test_1", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL, {"model": "model_test_1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(Car.objects.filter(model="model_test_1")))
        