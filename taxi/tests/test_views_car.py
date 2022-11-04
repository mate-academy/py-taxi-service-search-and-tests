from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            first_name="Jhon",
            last_name="Smith",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        mitsubishi = Manufacturer.objects.create(
            name="Mitsubishi", country="Japan")
        seat = Manufacturer.objects.create(name="Seat", country="Spain")
        Car.objects.create(model="Mitsubishi Lancer", manufacturer=mitsubishi)
        Car.objects.create(model="Seat Leon", manufacturer=seat)

        response = self.client.get(CAR_URL)
        car = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")
