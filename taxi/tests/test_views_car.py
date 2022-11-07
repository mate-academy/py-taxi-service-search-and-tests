from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford Motor Company",
            country="USA"
        )
        Car.objects.create(
            model="Ford Focus 4",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
