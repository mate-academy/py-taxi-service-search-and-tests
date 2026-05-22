from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer_name",
            country="manufacturer_country"
        )

        self.car = Car.objects.create(
            model="car_model",
            manufacturer=self.manufacturer
        )

    def test_list_view_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_detail_view_login_required(self):
        response = self.client.get(CAR_URL, args=[self.car.id])
        self.assertNotEquals(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer_name",
            country="manufacturer_country"
        )

    def test_retrieve_cars(self):
        Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(CAR_URL)
        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer_name",
            country="manufacturer_country"
        )

        self.car = Car.objects.create(
            model="car_model",
            manufacturer=self.manufacturer
        )

    def test_driver_search_by_model(self):
        response = self.client.get(CAR_URL, {"model": "car_model"})
        self.assertEquals(response.status_code, 200)

        cars = response.context["car_list"]
        self.assertEquals(len(cars), 1)
        self.assertEquals(cars[0].model, "car_model")

    def test_car_search_with_no_result(self):
        response = self.client.get(CAR_URL, {"model": "unknown"})
        cars = response.context["car_list"]
        self.assertEquals(len(cars), 0)
