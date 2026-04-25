from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="X5 M", manufacturer=manufacturer)
        Car.objects.create(model="X3", manufacturer=manufacturer)
        Car.objects.create(model="S", manufacturer=manufacturer)

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertEqual(len(response.context["car_list"]), 3)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search_with_results(self):
        query_params = {"model": "X"}
        response = self.client.get(CAR_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars.filter(model__icontains=query_params["model"]))
        )

    def test_car_search_without_results(self):
        query_params = {"model": "No results"}
        response = self.client.get(CAR_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            []
        )

    def test_car_create_successful(self):
        response = self.client.post(
            CAR_CREATE_URL,
            data={
                "model": "Test Model",
                "manufacturer": Car.objects.get(id=1).manufacturer.id,
                "drivers": [self.user.id],
            }
        )
        self.assertRedirects(response, reverse("taxi:car-list"))
