from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car

CARS_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_access(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(CARS_URL)
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )

    def test_filter(self):
        response = self.client.get(f"{CARS_URL}?model=X5")
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="X5")
        )
