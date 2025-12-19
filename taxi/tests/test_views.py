from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )

    def test_car_list_view_status_code(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_contains_car(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "X5")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"}
        )
        self.assertContains(response, "X5")


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer
        )

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A6")
