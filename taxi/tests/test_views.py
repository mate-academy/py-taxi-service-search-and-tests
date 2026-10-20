from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicCarTest(TestCase):
    def test_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country",
        )
        self.car_1 = Car.objects.create(
            model="Model",
            manufacturer=self.manufacturer,
        )
        self.user = get_user_model().objects.create(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_list(self):
        Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "b"}
        )
        expected_cars = Car.objects.filter(model__icontains="b")
        self.assertEqual(
            list(response.context["car_list"]),
            list(expected_cars)
        )

        self.assertIn("search_form", response.context)

        self.assertEqual(
            response.context["search_form"].initial["model"],
            "b"
        )
