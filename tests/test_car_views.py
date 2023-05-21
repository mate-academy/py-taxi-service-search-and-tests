from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):

    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "1233test22"
        )
        self.client.force_login(self.user)

    def test_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Car.objects.create(
            model="test2_model",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test1_model",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_search_car_(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Car.objects.create(model="test_model", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL, {"model": "test_model"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model="test_model"))
        )
