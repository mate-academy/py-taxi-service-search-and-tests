from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail_view_requires_login(self):
        res = self.client.get(reverse("taxi:car-detail", args=[self.car.id]))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Prius",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_context_data(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Prius"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["model"], "Prius")

    def test_get_queryset_with_search(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Prius"})
        cars = Car.objects.filter(model__icontains="Prius")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
