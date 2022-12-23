from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test", password="test12345"
        )
        self.client.force_login(self.user)

    def test_car_retrieve(self):
        Car.objects.create(
            model="RX8",
            manufacturer=Manufacturer.objects.create(
                name="Mazda",
                country="Japan"),
        )

        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]),
                         list(Car.objects.all()))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def car_test_create(self):
        form_data = {
            "model": "Test",
            "manufacturer": Manufacturer.objects.create(
                name="Test",
                country="TEst"),
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.name,
                         form_data["manufacturer"].name)
        self.assertEqual(
            new_car.manufacturer.country, form_data["manufacturer"].country
        )
