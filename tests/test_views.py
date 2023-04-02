from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class UserAndManufacturerSetUp:
    def generate_data(self):
        self.user = get_user_model().objects.create(
            username="test",
            password="1234asdf",
            license_number="LLL23456"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )


class PublicCarListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarListTest(TestCase, UserAndManufacturerSetUp):
    def setUp(self) -> None:
        self.generate_data()
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)


class AssignToCarTest(TestCase, UserAndManufacturerSetUp):
    def setUp(self) -> None:
        self.generate_data()
        self.client.force_login(self.user)

    def test_assign_new_driver_to_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.user.cars.all())

    def test_removed_driver_from_car(self):
        self.user.cars.add(self.car)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.user.cars.all())
