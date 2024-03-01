from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_FORMAT_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_cars(self):
        manufacturer = Manufacturer.objects.create(name="Toyota")
        car1 = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        car2 = Car.objects.create(model="Camry", manufacturer=manufacturer)
        response = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )
