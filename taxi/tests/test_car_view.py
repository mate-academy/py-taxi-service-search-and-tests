from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test.user",
            "user12345",
        )
        self.client.force_login(self.user)

    def test_car_list_response_with_correct_template(self):
        response = self.client.get(CARS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Chevrolet", country="USA")
        Car.objects.create(model="Camry", manufacturer_id=1)
        Car.objects.create(model="Cruise", manufacturer_id=2)
        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail_with_new_car(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Camry", manufacturer_id=1)
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_search_car_form(self):
        response = self.client.get(CARS_URL + "?model=RX-8")

        self.assertContains(response, "RX-8")
        self.assertNotContains(response, "626")
        self.assertTemplateUsed(response, "taxi/car_list.html")
