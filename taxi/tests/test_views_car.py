from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Prius", manufacturer=self.manufacturer)

    def test_car_list_view_status_code(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_template_used(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_view_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Corolla"}
        )
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Prius")
