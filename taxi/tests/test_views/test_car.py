from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )

    def test_car_list_login_required(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(reverse(
            "taxi:car-detail", kwargs={"pk": self.car.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(reverse(
            "taxi:car-delete", kwargs={"pk": self.car.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(reverse(
            "taxi:car-update", kwargs={"pk": self.car.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        self.car = Car.objects.create(
            model="test_model1",
            manufacturer=manufacturer,
        )

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_car_list_login_required(self):
        response = self.client.get(CARS_URL)

        self.assertEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(reverse(
            "taxi:car-detail", kwargs={"pk": self.car.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(reverse(
            "taxi:car-delete", kwargs={"pk": self.car.id}
        ))
        self.assertEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(reverse(
            "taxi:car-update", kwargs={"pk": self.car.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context["car_list"]),
            list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
