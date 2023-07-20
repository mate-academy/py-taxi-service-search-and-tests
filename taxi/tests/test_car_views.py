from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):

        car = car_create()

        car_detail_url = reverse("taxi:car-detail", kwargs={"pk": car.pk})

        car_urls = [CAR_LIST_URL, car_detail_url]

        for url in car_urls:
            response = self.client.get(url)

            self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_1234"
        )

        self.client.force_login(self.user)

        self.car = car_create()

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        car_detail_url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})

        response = self.client.get(car_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["car"],
            self.car
        )
        self.assertTemplateUsed(response, "taxi/car_detail.html")


def car_create():
    manufacturer = Manufacturer.objects.create(
        name="test",
        country="test_country"
    )

    Car.objects.create(model="test_model_1",
                       manufacturer=manufacturer)
    return Car.objects.create(model="test_model_2",
                              manufacturer=manufacturer)
