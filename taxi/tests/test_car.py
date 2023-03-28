from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_car_list_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        url = reverse("taxi:manufacturer-update", args=[car.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        url = reverse("taxi:manufacturer-delete", args=[car.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_retrieve_car_list(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)

        url = reverse("taxi:car-list")
        response = self.client.get(url)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_retrieve_car_detail_page(self):
        car = Car.objects.create(model="Camry", manufacturer=self.manufacturer)

        url = reverse("taxi:car-detail", args=[car.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_car_search_by_model(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="RAV4", manufacturer=self.manufacturer)

        url = reverse("taxi:car-list") + "?model=c"
        response = self.client.get(url)

        cars_contains_a = Car.objects.filter(model__icontains="c")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars_contains_a)
        )

    def test_car_create(self):
        data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": self.user.id
        }
        url = reverse("taxi:car-create")
        response = self.client.post(url, data=data)

        self.assertEqual(Car.objects.last().model, "Camry")
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_car_update(self):
        car = Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        data = {
            "model": "Corolla",
            "manufacturer": car.manufacturer.id,
            "drivers": self.user.id
        }
        url = reverse("taxi:car-update", args=[car.id])
        response = self.client.post(url, data=data)

        self.assertEqual(Car.objects.get(id=car.id).model, "Corolla")
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_car_delete(self):
        car = Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        url = reverse("taxi:car-delete", args=[car.id])
        response = self.client.post(url)

        cars = Car.objects.all()

        self.assertFalse(car in cars)
        self.assertRedirects(response, reverse("taxi:car-list"))
