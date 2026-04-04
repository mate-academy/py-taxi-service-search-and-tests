from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testuser1",
        )
        self.client.force_login(self.user)
        manufacture = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Corolla", manufacturer=manufacture)
        Car.objects.create(model="Camry", manufacturer=manufacture)
        Car.objects.create(model="Supra", manufacturer=manufacture)

    def test_search_by_model_icontains(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=cor")
        self.assertEqual(response.status_code, 200)
        cars = response.context["object_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Corolla")
