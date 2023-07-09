from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateCarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
