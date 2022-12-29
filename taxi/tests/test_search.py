from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_of_searching_cars(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list") + "?model=A6"
        )

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="A6")),
        )
