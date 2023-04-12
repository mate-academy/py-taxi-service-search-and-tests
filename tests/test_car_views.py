from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Daewoo", country="Ukraine"
        )
        self.car1 = Car.objects.create(
            model="Lanos", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Slavuta", manufacturer=self.manufacturer
        )

    def test_car_list(self) -> None:
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search(self) -> None:
        response = self.client.get(CAR_URL, {"model": "lan"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertNotContains(response, "Slavuta")
        self.assertContains(response, "Lanos")

    def test_car_detail(self) -> None:
        url = reverse("taxi:car-detail", args=[self.car1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertContains(response, self.car1.id)
