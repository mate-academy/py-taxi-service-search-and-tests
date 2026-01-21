from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car1 = Car.objects.create(
            model="Q5",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Bronco",
            manufacturer=self.manufacturer2,
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_get_context_data(self):
        response = self.client.get(CAR_LIST_URL, {"model": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertEqual(
            response.context_data["search_form"].initial["model"], "test"
        )

    def test_get_query_with_no_filters(self):

        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)

    def test_get_query_with_filters(self):
        response = self.client.get(CAR_LIST_URL, {"model": self.car1.model})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
