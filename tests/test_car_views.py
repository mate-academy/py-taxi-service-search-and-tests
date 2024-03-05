from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer

MANUFACTURER_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="testManufacturer"
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_all_drivers(self) -> None:
        Car.objects.create(model="Test Car 1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test Car 2", manufacturer=self.manufacturer)
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
